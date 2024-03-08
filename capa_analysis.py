from flask import Blueprint, request, jsonify, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
import subprocess
import json
import os
from concurrent.futures import ProcessPoolExecutor
import hashlib
from datetime import datetime
from flask_login import current_user
import logging, magic

capa_analysis_bp = Blueprint('capa_analysis', __name__)
MAX_FILE_SIZE = 3 * 1024 * 1024  # 3MB

ALLOWED_MIME_TYPES = [
    'application/vnd.microsoft.portable-executable', 
    'application/x-dosexec'
]


def allowed_file(filename):
    """Check if the file extension is allowed."""
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    
def find_and_extract(json_data, target_key):
    """
    Recursively search for a target key in nested JSON and extract the value.

    :param json_data: The JSON data to search through.
    :param target_key: The key you're looking for.
    :return: The extracted data or None if the key isn't found.
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                return value  # Return the entire section from here
            else:
                result = find_and_extract(value, target_key)  # Recursive call
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_and_extract(item, target_key)  # Recursive call
            if result is not None:
                return result

    return None  # Key not found
        
def deep_search(data, target_keys):
    """
    Recursively search for keys in nested JSON and accumulate their values.
    
    :param data: The JSON data to search through.
    :param target_keys: A set of keys to search for.
    :return: A dictionary with keys and their found values.
    """
    results = {}
    
    def recurse(sub_data, path=[]):
        if isinstance(sub_data, dict):
            for k, v in sub_data.items():
                if k in target_keys:
                    results[k] = v
                recurse(v, path + [k])
        elif isinstance(sub_data, list):
            for item in sub_data:
                recurse(item, path + [str(sub_data.index(item))])
    
    recurse(data)
    return results

def get_user_team(username):
    team_name = "Default Team"  # Default if no matching team is found

    try:
        # Load users data
        with open('users.json', 'r') as f:
            users_data = json.load(f)
        users = users_data.get('users', [])


        # Load teams data
        with open('teams.json', 'r') as f:
            teams_data = json.load(f)
        teams = teams_data.get('teams', [])


        # Find user's team ID
        user_team_id = None
        for user in users:
            if user.get('username') == username:
                user_team_id = user.get('team_id')
                break
        
        print(f"Team ID for user '{username}':", user_team_id)  # Debugging line

        # Match team ID with team name
        if user_team_id is not None:
            for team in teams:
                if str(team.get('id')) == str(user_team_id):
                    team_name = team.get('name')
                    break

    except Exception as e:
        print(f"Error reading JSON data: {e}")

    print(f"Team name for user '{username}':", team_name)  # Debugging line
    return team_name


    # Debug: Print the found team name
    print(f"Team name for user {username}: {team_name}")
    return team_name
    
def record_analysis_history(team_name, filename, timestamp, file_hash, save_path, extracted_data):
    try:
        with open('analysis_history.json', 'r') as file:
            history_data = json.load(file)
    except FileNotFoundError:
        history_data = {"analysis": []}

    team_entry = next((entry for entry in history_data["analysis"] if entry["team_name"] == team_name), None)
    if not team_entry:
        team_entry = {"team_name": team_name, "history": []}
        history_data["analysis"].append(team_entry)

    # Prepare the rules summary for inclusion
    rules_summary = extracted_data.get("rules_summary", {})
    # Create a simplified version of the rules summary for history record
    simplified_rules_summary = {
        rule: {
            "description": details.get("description"),
            "authors": details.get("authors"),
            "reference_count": details.get("reference_count"),
            "match_count": details.get("match_count")
        } for rule, details in rules_summary.items()
    }

    new_record = {
        "file_name": filename,
        "timestamp": timestamp,
        "file_hash": file_hash,
        "save_path": save_path,
        "extracted_data": simplified_rules_summary  # Include the simplified rules summary directly
    }
    team_entry["history"].append(new_record)

    with open('analysis_history.json', 'w') as file:
        json.dump(history_data, file, indent=4)


def extract_windows_api(capa_result):
    """
    Extracts Windows API calls marked with success from CAPA results.
    
    Args:
        capa_result (dict): The CAPA result as a Python dictionary.
        
    Returns:
        list: A list of dictionaries, each containing the API name and the rule it came from.
    """
    windows_api_calls = []

    if "rules" in capa_result:
        for rule_name, rule_details in capa_result["rules"].items():
            # Assuming 'features' is a list of features under each rule.
            for feature in rule_details.get("features", []):
                # Check if feature is successful and is of type 'api'.
                if feature.get("success") and "api" in feature.get("node", {}).get("feature", {}):
                    api_name = feature["node"]["feature"]["api"]
                    windows_api_calls.append({"api_name": api_name, "rule_name": rule_name})

    return windows_api_calls

def extract_successful_windows_api(capa_result):
    successful_apis = []
    
    # Iterate through each rule in the CAPA results
    for rule_details in capa_result.get("rules", {}).values():
        # Check if the rule has matches and iterate through them
        for match in rule_details.get("matches", []):
            # Iterate through each match detail, looking for successful API calls
            for match_detail in match:
                # Extract the feature details, specifically looking for API calls
                feature = match_detail.get("node", {}).get("feature", {})
                if match_detail.get("success") and feature.get("type") == "api":
                    api_name = feature["api"]
                    successful_apis.append(api_name)
    
    return successful_apis



def deduplicate_items(items):
    """
    Deduplicate a list of items which could be dictionaries, ensuring uniqueness.
    If items are dictionaries or lists, it deduplicates based on their content.
    """
    seen = set()
    deduplicated = []
    for item in items:
        # Convert item to a hashable form
        hashable_item = make_hashable(item)
        if hashable_item not in seen:
            seen.add(hashable_item)
            deduplicated.append(item)
    return deduplicated

def make_hashable(item):
    """Recursively make item hashable if it's a list or a dictionary."""
    if isinstance(item, dict):
        return frozenset((k, make_hashable(v)) for k, v in item.items())
    elif isinstance(item, list):
        return tuple(make_hashable(e) for e in item)
    else:
        return item

def extract_data_from_capa_result(capa_result):

    # Initialize the structure for the extracted data with pre-populated fields
    extracted_data = {
        "md5": capa_result["meta"]["sample"]["md5"],
        "sha1": capa_result["meta"]["sample"]["sha1"],
        "sha256": capa_result["meta"]["sample"]["sha256"],
        "path": capa_result["meta"]["sample"]["path"],
        "flavor": capa_result["meta"]["flavor"],
        "format": capa_result["meta"]["analysis"]["format"],
        "arch": capa_result["meta"]["analysis"]["arch"],
        "os": capa_result["meta"]["analysis"]["os"],
        "file_hash": capa_result["meta"]["sample"]["sha256"],
        "ATT&CK": [],
        "MBC": [],
        "capabilities": [],
        "windows_api": []  # Added field for Windows API
    }


    if "rules" in capa_result:
        for rule_name, rule_details in capa_result["rules"].items():
            meta = rule_details.get("meta", {})

            # For 'ATT&CK'
            if 'attack' in meta:
                for attack in meta['attack']:
                    extracted_data["ATT&CK"].append(attack)

            # For 'MBC'
            if 'mbc' in meta:
                for mbc in meta['mbc']:
                    extracted_data["MBC"].append(mbc)

            # Extract rule name as capability
            capability_info = {
                "name": rule_name,
                "description": meta.get("description", "No description available."),
                "references": meta.get("references", []),
                "authors": meta.get("authors", [])
            }
            extracted_data["capabilities"].append(capability_info)

    # Deduplicate 'ATT&CK', 'MBC', 'capabilities'
    extracted_data["ATT&CK"] = deduplicate_items(extracted_data["ATT&CK"])
    extracted_data["MBC"] = deduplicate_items(extracted_data["MBC"])
    extracted_data["capabilities"] = deduplicate_items(extracted_data["capabilities"])

    # Extract and integrate Windows API calls
    windows_api_calls = extract_windows_apis(capa_result)  # Assuming this function is similar to the pseudo-code provided
    extracted_data["windows_api"].extend(windows_api_calls)
    extracted_data["windows_api"] = deduplicate_items(extracted_data["windows_api"])


    return extracted_data

def extract_windows_apis(capa_result):
    windows_apis = []
    # Iterate through each rule in the capa_result
    for rule_name, rule_details in capa_result.get("rules", {}).items():
        # Check for matches within each rule
        for match in rule_details.get("matches", []):
            # Iterate through matches to find API calls
            for match_detail in match:
                api_name = match_detail.get("node", {}).get("feature", {}).get("api")
                if api_name:
                    windows_apis.append(api_name)
    # Return a list of unique API calls
    return list(set(windows_apis))
    



    

def run_capa_analysis(file_path, capa_rules_path):
    result = subprocess.run(['capa', '-r', capa_rules_path, '-j', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

@capa_analysis_bp.route('/analyze', methods=['GET', 'POST'])
def analyze_file():
    capa_rules_path = current_app.config['CAPA_RULES_PATH']
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'No selected file or file type not allowed'}), 400

    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    if file_length > MAX_FILE_SIZE:
        return jsonify({'error': 'File exceeds maximum size limit'}), 400

    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if mime_type not in ALLOWED_MIME_TYPES:
        return jsonify({'error': 'File MIME type not allowed'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    with ProcessPoolExecutor() as executor:
        future = executor.submit(run_capa_analysis, file_path, capa_rules_path)
        result = future.result()

    if result.returncode != 0:
        os.remove(file_path)  # Cleanup
        return jsonify({'error': 'CAPA encountered an error', 'details': result.stderr}), 500

    try:
        capa_result = json.loads(result.stdout)

        extracted_data = extract_data_from_capa_result(capa_result)
        team_name = get_user_team(current_user.username) if get_user_team(current_user.username) else "Default Team"

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Save extracted data to JSON file
        json_filename = generate_filename(filename, timestamp, 'json')
        json_filepath = os.path.join(current_app.config['ANALYSIS_FILES_FOLDER'], json_filename)
        with open(json_filepath, 'w') as json_file:
            extracted_data['timestamp'] = timestamp
            extracted_data['file_hash'] = file_hash
            json.dump(extracted_data, json_file, indent=4)
            logging.info(f"Analysis result saved as JSON file: {json_filepath}")

            # Optionally record analysis history
            record_analysis_history(team_name, filename, timestamp, file_hash, json_filepath, extracted_data)

        os.remove(file_path)  # Cleanup after processing
        logging.info(f"Uploaded file {filename} removed after processing.")
        flash('File successfully uploaded and analyzed', 'success')
        return redirect(url_for('team_page', team_name=team_name))

    except json.JSONDecodeError as e:
        os.remove(file_path)
        flash('Failed to decode CAPA JSON output', 'error')
        return redirect(url_for('upload_and_analyze'))

        
def generate_filename(original_filename, timestamp, extension):
    basename, _ = os.path.splitext(original_filename)
    return f"{basename}_{timestamp}.{extension}"

    