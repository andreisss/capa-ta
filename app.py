from functools import wraps
import json
import logging
import math
import os
import pytz
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from multiprocessing import Pool
import hashlib
from flask import (
    Flask,
    abort,
    session,
    current_app as app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from auth import auth_bp
from capa_analysis import capa_analysis_bp
from config import Config
from models import User


# Set the logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register blueprint for capa-analysis
app.register_blueprint(capa_analysis_bp, url_prefix='/capa-analysis')

# Configure database file path
app.config['DATABASE_FILE'] = 'users.json'

# Set base directory
app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/update_admin_password', methods=['POST'])
def update_admin_password():
    if not is_admin():
        flash('Only admin can perform this action.', 'danger')
        return redirect(url_for('login'))

    # Assuming the request contains JSON with the new password
    new_password_plain = request.json.get('new_password')
    if not new_password_plain:
        return jsonify({'error': 'Missing new password'}), 400
    
    new_password_hashed = generate_password_hash(new_password_plain)

    data = read_database()
    admin_updated = False
    for user in data['users']:
        if user['id'] == 1 and user['role'] == 'admin':
            user['password'] = new_password_hashed
            admin_updated = True
            break

    if admin_updated:
        write_database(data)
        return jsonify({'message': 'Admin password updated successfully'}), 200
    else:
        return jsonify({'error': 'Admin user not found'}), 404

def teams():
    if request.method == 'GET':
        data = read_database()
        return jsonify(data['teams'])
    
    if request.method == 'POST':
        new_team = request.json
        data = read_database()
        data['teams'].append(new_team)
        write_database(data)
        return jsonify(new_team), 201
        

def edit_user():
    user_id = request.json.get('id')
    new_user_name = request.json.get('name')
    new_team_id = request.json.get('team_id')

    # Validate input data
    if not all([user_id, new_user_name, new_team_id]):
        return jsonify({'error': 'Missing data'}), 400

    # Attempt to edit the user
    success = edit_person(user_id, new_user_name, new_team_id)
    if success:
        return jsonify({'message': 'User edited successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

def edit_person(user_id, new_user_name, new_team_id):
    data = read_database()
    user_found = False
    for user in data['users']:
        if user['id'] == user_id:
            user['name'] = new_user_name
            user['team_id'] = new_team_id
            user_found = True
            break
    if user_found:
        write_database(data)
        return True
    return False

@login_manager.user_loader
def load_user(user_id):
    # Fetch the user data from 'users.json' using the static method `get` defined in the User class.
    return User.get(user_id)
    

   
def is_admin():
    # Assuming an 'is_admin' flag is stored in the session upon login
    return session.get('is_admin', False)



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming 'role' attribute in 'current_user' indicates user role
        # And 'admin' is the role indicating an admin user
        if not current_user.is_authenticated or getattr(current_user, 'role', None) != 'admin':
            flash('You need to be an admin to view this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def localize_timestamps(records, target_timezone='Europe/Paris'):
    """
    Adjusts the timestamps in the records to a specified time zone and formats them for display.
    :param records: List of dictionaries containing the report data.
    :param target_timezone: String name of the target time zone for conversion.
    :return: The adjusted records with timestamps formatted for display.
    """
    tz = pytz.timezone(target_timezone)
    for record in records:
        # Assume 'timestamp' is in UTC and in '%Y-%m-%d %H:%M:%S' format
        utc_dt = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        local_dt = utc_dt.astimezone(tz)
        # Format for display, e.g., '2024-02-27 01:12:37 PM CEST'
        record['timestamp'] = local_dt.strftime('%Y-%m-%d %I:%M:%S %p %Z')
    return records
    


 
 
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

   
@app.route('/settings')
def settings():
    # Read the settings from the file again in case they were updated
    with open('settings.json') as json_file:
        current_settings = json.load(json_file)
    return render_template('settings.html', settings=current_settings)

# Load settings from settings.json
with open('settings.json') as json_file:
    app.config.update(json.load(json_file))

@app.route('/settings')
def show_settings():
    # Load current settings from settings.json
    with open('settings.json') as f:
        current_settings = json.load(f)
    
    # Pass the settings to the HTML template
    return render_template('settings.html', settings=current_settings)

# Update settings from settings.json
def update_app_config():
    """Reloads settings from settings.json into app.config."""
    try:
        with open('settings.json') as json_file:
            settings = json.load(json_file)
            
        # Updating app.config with settings from settings.json
        app.config['UPLOAD_FOLDER'] = settings.get('UPLOAD_FOLDER', app.config['UPLOAD_FOLDER'])
        app.config['CAPA_RULES_PATH'] = settings.get('CAPA_RULES_PATH', app.config['CAPA_RULES_PATH'])
        app.config['SECRET_KEY'] = settings.get('SECRET_KEY', app.config['SECRET_KEY'])
        app.config['ALLOWED_EXTENSIONS'] = settings.get('ALLOWED_EXTENSIONS', app.config['ALLOWED_EXTENSIONS'])
        app.config['ANALYSIS_FILES_FOLDER'] = settings.get('ANALYSIS_FILES_FOLDER', app.config['ANALYSIS_FILES_FOLDER'])
        app.config['ADMIN_PASS'] = settings.get('ADMIN_PASS', app.config['ADMIN_PASS'])
    except FileNotFoundError as e:
        print(f"Error loading settings from settings.json: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding settings.json: {e}")

# Ensure to call update_app_config() at application start to load initial settings
update_app_config()


@app.route('/update_settings', methods=['POST'])
def update_settings():
    app.logger.info('Received settings update request')  # Log the start of the operation

    data = request.get_json()  # Parse JSON data from request
    if not data:
        app.logger.error('Invalid or missing JSON data')  # Log error if data is missing or invalid
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    # Logging received form data for debugging purposes
    app.logger.info(f'Received form data: {data}')

    new_settings = {
        'UPLOAD_FOLDER': data.get('upload_folder'),
        'CAPA_RULES_PATH': data.get('capa_rules_path'),
        'SECRET_KEY': data.get('secret_key'),
        'ALLOWED_EXTENSIONS': data.get('allowed_extensions'),
        'ANALYSIS_FILES_FOLDER': data.get('analysis_files_folder'),
        'ADMIN_PASS': data.get('admin_pass'),
        'VIRUSTOTAL_API_KEY': data.get('virustotal_api_key')
    }

    # Your existing logic to update settings

    # Persist new settings to settings.json
    try:
        with open('settings.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        app.logger.error('Failed to update settings.json: %s', str(e))
        return jsonify({'error': 'Failed to persist settings'}), 500

    app.logger.info('Settings updated successfully: %s', data)
    return jsonify({'message': 'Settings updated successfully!'})


# Ensure to call update_app_config() at application start to load initial settings
update_app_config()  

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        data = read_database()
        return jsonify(data['users'])
    
    if request.method == 'POST':
        new_user = request.json
        data = read_database()
        data['users'].append(new_user)
        write_database(data)
        return jsonify(new_user), 201

# Your login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('login.html')

        user = User.get_by_username(username)

        if user and check_password_hash(user.password, password):
            login_user(user)  # Log in the user
            session['logged_in'] = True
            session['username'] = user.username
            session['role'] = user.role

            flash(f'You were successfully logged in as {user.role}.', 'success')
            app.logger.info(f'Successful login for user: {user.username} as {user.role}')

            if user.role == 'admin':
                return redirect(url_for('admin_console'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

def get_teams_by_username(username):
    """Fetch teams for a user based on their username from teams.json."""
    teams_info = []  # Correct variable name initialization
    with open('teams.json') as f:
        data = json.load(f)
        # Iterate through 'users' to find matching 'username' and its 'team_id'
        for user in data["users"]:
            if user["name"] == username:
                # Find the team in 'teams' that matches the 'team_id'
                team_info = next((team for team in data["teams"] if team["id"] == user["team_id"]), None)
                if team_info:
                    teams_info.append(team_info)
    return teams_info  # Ensure the correct variable name is used here

@app.route('/admin_console')
@login_required
def admin_console():
    if not current_user.is_authenticated or getattr(current_user, 'role', None) != 'admin':
        flash('Access denied: Admins only.', 'warning')
        return redirect(url_for('home'))

    try:
        with open('teams.json') as f:
            teams_data = json.load(f)['teams']
        with open('users.json') as f:
            users_data = json.load(f)['users']
        
        return render_template('admin_console.html', teams=teams_data, users=users_data)
    except Exception as e:
        flash(f'Error loading data: {e}', 'danger')
        return redirect(url_for('home'))

        
        
        
@app.route('/team/<int:team_id>/details')
@login_required
def team_details(team_id):
    team_info = get_team_info(team_id)  # Your existing logic
    capa_history = get_capa_history(team_id)  # Your existing logic
    
    # Convert and format timestamps
    for item in capa_history:
        # Assuming 'timestamp' is a string in UTC: '2024-02-27 01:12:37'
        utc_time = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
        utc_time = utc_time.replace(tzinfo=pytz.utc)  # Set timezone to UTC
        cet_time = utc_time.astimezone(pytz.timezone('CET'))  # Convert to CET
        item['timestamp'] = cet_time.strftime('%Y-%m-%d %I:%M:%S %p CET')  # Format
    
    # Sort the analysis history based on timestamp in descending order
    analysis_history_sorted = sorted(get_analysis_history(team_id), key=lambda x: x.get('timestamp'), reverse=True)

    return render_template('team_details.html', team_info=team_info, capa_history=capa_history, analysis_history=analysis_history_sorted)       
        
def save_analysis(file, team_name):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_hash = hashlib.sha256(file.read()).hexdigest()
    # Reset file pointer after reading for hash calculation
    file.seek(0)
    
    # Generate a random identifier for the file
    random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    file_name = f"{random_id}.analysis"
    
    # Assuming you have a directory to save analysis files
    save_path = os.path.join('analysis_files', team_name, file_name)
    file.save(save_path)
    
    # Save analysis details to database or a file
    record_analysis_history(team_name, file_name, timestamp, file_hash, save_path)
    
    return file_name, timestamp, file_hash
    

                           
def get_analysis_history_for_team_paginated(team_name, page=1, per_page=10):
    try:
        with open('analysis_history.json', 'r') as f:
            analysis_data = json.load(f).get('analysis', [])

        # Find the team with the matching 'team_name'
        team_data = next((item for item in analysis_data if item.get('team_name', '').lower() == team_name.lower()), None)

        if team_data:
            history = team_data.get('history', [])
            # Sort the history based on timestamp in descending order
            sorted_history = sorted(history, key=lambda x: x.get('timestamp'), reverse=True)
            # Calculate start and end indices for the current page
            start = (page - 1) * per_page
            end = start + per_page
            # Paginate the sorted history list
            paginated_history = sorted_history[start:end]
            return paginated_history, len(history)
        else:
            print(f"No history found for team: {team_name}")
            return [], 0
    except Exception as e:
        print(f"Error reading analysis_history.json: {e}")
        return [], 0




def generate_filename(original_filename, suffix, extension):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    basename, _ = os.path.splitext(original_filename)
    return f"{basename}_{timestamp}_{suffix}.{extension}"
    

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.basicConfig(level=logging.DEBUG)
    if 'file' not in request.files:
        logging.error('No file part')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            logging.info(f'File saved to {file_path}')
            
            # Analyze the file and get results
            analysis_results = analyze_file(file_path)
            
            # Save analysis results to a JSON file
            json_filename = generate_filename(filename, 'analysis', 'json')
            json_path = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)
            with open(json_path, 'w') as json_file:
                json.dump(analysis_results, json_file)
            logging.info(f'Analysis results saved to {json_path}')
            
            # Optionally, generate a downloadable file based on analysis
            download_filename = generate_filename(filename, 'download', 'txt')  # Change extension as needed
            download_path = os.path.join(app.config['UPLOAD_FOLDER'], download_filename)
            with open(download_path, 'w') as download_file:
                download_file.write("Your analysis results...\n")  # Customize content based on analysis
            logging.info(f'Downloadable file generated at {download_path}')
            
        except Exception as e:
            logging.error(f'Failed to save file: {e}')
            return jsonify({'error': 'Failed to save file'}), 500

        return jsonify({'message': 'File successfully uploaded and analyzed', 'filename': filename, 'analysis_file': json_filename, 'download_file': download_filename}), 200


@app.route('/view_report/<file_hash>')
@login_required
def view_report(file_hash):
    reports_directory = app.config['ANALYSIS_FILES_FOLDER']
    logging.info(f'Attempting to find report with file hash: {file_hash}')
    
    for filename in os.listdir(reports_directory):
        if filename.endswith('.json'):
            with open(os.path.join(reports_directory, filename), 'r') as file:
                try:
                    data = json.load(file)
                    if 'file_hash' in data and data['file_hash'] == file_hash:
                        logging.info(f'Found matching report file: {filename}')
                        return render_template('report_template.html', report=data, report_data=json.dumps(data))
                except json.JSONDecodeError:
                    logging.error(f'Failed to parse JSON in file: {filename}')
                    continue

    logging.error('Report not found')
    return 'Report not found', 404


@app.route('/download_report/<file_hash>')
def download_report(file_hash):
    reports_directory = app.config['ANALYSIS_FILES_FOLDER']
    logging.info(f'Attempting to find report with file hash: {file_hash}')
    
    for filename in os.listdir(reports_directory):
        if filename.endswith('.json'):
            with open(os.path.join(reports_directory, filename), 'r') as file:
                try:
                    data = json.load(file)
                    if 'file_hash' in data and data['file_hash'] == file_hash:
                        logging.info(f'Found matching report file: {filename}')
                        return send_from_directory(reports_directory, filename)
                except json.JSONDecodeError:
                    logging.error(f'Failed to parse JSON in file: {filename}')
                    continue

    logging.error('Report not found')
    return 'Report not found', 404
    
    
def find_report_by_hash(file_hash):
    reports_directory = app.config['ANALYSIS_FILES_FOLDER']

    for filename in os.listdir(reports_directory):
        if file_hash in filename:
            return os.path.join(reports_directory, filename)

    return None

@app.route('/analysis_files/<filename>')
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': 'File not found or unable to download'}), 404     
       

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

    return team_name
    
@app.route('/team/<team_name>')
@login_required
def team_page(team_name):
    # Check if the current user belongs to the team they're trying to access
    user_team = get_user_team(current_user.username)  # Assuming this returns the team name
    if user_team != team_name:
        flash('You do not have permission to access this team page.', 'warning')
        return redirect(url_for('user_dashboard'))  # Redirect them to a general page like the dashboard

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  # Adjust per_page as needed

    team_data = get_team_data(team_name)
    if not team_data:
        return "Team not found", 404

    analysis_history, total_pages = get_analysis_history_for_team_paginated(team_name, page, per_page)

    return render_template('team_page.html', team_data=team_data, analysis_history=analysis_history, page=page, total_pages=total_pages)


@app.route('/capa-analysis/analyze', methods=['POST'])
@login_required
def upload_and_analyze():
    capa_rules_path = current_app.config['CAPA_RULES_PATH']
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File not allowed'}), 400

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
        extracted_data['payload'] = capa_result.get('payload', '')

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

            record_analysis_history(team_name, filename, timestamp, file_hash, json_filepath, extracted_data)

        os.remove(file_path)  # Cleanup after processing
        logging.info(f"Uploaded file {filename} removed after processing.")
        flash('File successfully uploaded and analyzed', 'success')
        return redirect(url_for('team_page', team_name=team_name))

    except json.JSONDecodeError as e:
        os.remove(file_path)
        flash('Failed to decode CAPA JSON output', 'error')
        return redirect(url_for('upload_and_analyze'))

@app.route('/download_json/<path:filename>')
def download_json(filename):
    # Ensure the requested file is within the allowed directory
    json_folder = current_app.config['ANALYSIS_FILES_FOLDER']
    if not os.path.isabs(filename) and filename.startswith(json_folder):
        return send_from_directory(json_folder, filename)
    else:
        return jsonify({'error': 'Invalid file path'}), 400
        
        
def generate_filename(original_filename, timestamp, extension):
    basename, _ = os.path.splitext(original_filename)
    return f"{basename}_{timestamp}.{extension}"
        

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    user_teams = []  # List to hold team info dictionaries
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
            users_data = data["users"]

        current_user_data = next((user for user in users_data if user['username'] == current_user.username), None)
        
        if current_user_data:
            # Assuming teams.json structure similar to users.json for demonstration
            with open('teams.json', 'r') as f:
                teams_data = json.load(f)["teams"]
                user_team = next((team for team in teams_data if str(team['id']) == str(current_user_data.get('team_id'))), None)
                if user_team:
                    # Add team name and URL to the list
                    user_teams.append({
                        'name': user_team['name'],
                        'url': url_for('team_page', team_name=user_team['name'])  # Assuming the route for team pages
                    })
    except Exception as e:
        print(f"Failed to process users.json or teams.json: {e}")
    
    return render_template('user_dashboard.html', user_teams=user_teams, username=current_user.username)

def get_user_reports(user_id):
    # Placeholder function to fetch user-specific reports
    # Implement logic to fetch data from your database or data source
    return user_reports

def get_team_capa_analysis(team_id):
    # Placeholder function to fetch team capability analysis data
    # Implement logic to fetch data from your database or data source
    return team_capa_analysis


def get_team_data(team_name):
    try:
        with open('teams.json', 'r') as f:
            teams_data = json.load(f).get('teams', [])
        with open('users.json', 'r') as f:
            users_data = json.load(f).get('users', [])
    except Exception as e:
        raise IOError(f"Error reading JSON files: {e}")
    
    # Find the team by name
    team = next((team for team in teams_data if team.get('name') == team_name), None)
    if not team:
        return None
    
    # Enrich the team data with user information
    team_users = [user for user in users_data if str(user.get('team_id')) == str(team.get('id'))]
    for user in team_users:
        user['team_name'] = team_name  # Add team name to each user
    
    # Add the users to the team data
    team['users'] = team_users
    
    return team




@app.route('/logout', methods=['POST'])
def logout():
    logout_user()  # Log out the user
    session.clear()  # Clears the session
    flash('You have been logged out.')
    return redirect(url_for('login'))



    
@app.route('/')
def home():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Further check if the user is an admin to decide on redirection
        if getattr(current_user, 'role', None) == 'admin':
            return redirect(url_for('admin_console'))
        else:
            return redirect(url_for('user_dashboard'))
    else:
        return redirect(url_for('login'))
    
     

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_form():
    return render_template('upload.html')
    
def find_user_by_id(user_id):
    try:
        with open('users.json', 'r') as f:
            users_data = json.load(f)
            for user in users_data.get('users', []):
                # Ensure IDs are compared as the same type (int)
                if user['id'] == user_id:
                    return user
    except FileNotFoundError:
        print("The users.json file was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from users.json.")
    
    return None
    
@app.route('/team/<int:team_id>/members', methods=['GET'])
def list_team_members(team_id):
    # Logic to list all members of a team based on 'team_id'
    return jsonify(members), 200


@app.route('/create_team', methods=['POST'])
def create_team():
    data = request.get_json()
    new_team = {
        # Generate a new ID for the team. This is a simple example.
        'id': None,  # You'll need to calculate this based on existing IDs.
        'name': data['name']
    }

    with open('teams.json', 'r+') as f:
        teams_data = json.load(f)
        if not teams_data.get('teams'):
            teams_data['teams'] = []
        # Simple ID generation: find the max ID and add 1
        new_team['id'] = 1 if not teams_data['teams'] else max(team['id'] for team in teams_data['teams']) + 1
        teams_data['teams'].append(new_team)
        
        f.seek(0)
        json.dump(teams_data, f, indent=4)
        f.truncate()

    return jsonify({'message': 'Team created successfully'}), 200
    
@app.route('/delete_team/<int:team_id>', methods=['POST'])
@login_required
def delete_team(team_id):
    # Your logic to delete the team from the database or JSON file
    # Example: Delete team from a JSON file (simplified for illustration)
    with open('teams.json', 'r+') as file:
        teams = json.load(file)
        teams['teams'] = [team for team in teams['teams'] if team['id'] != team_id]
        file.seek(0)
        json.dump(teams, file, indent=4)
        file.truncate()
    return jsonify({'message': 'Team deleted successfully'}), 200




@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not all(key in data for key in ['name', 'team_id', 'password']):
        logging.error("Missing required fields")
        return jsonify({'error': 'Missing name, team_id, or password'}), 400

    try:
        team_id = int(data['team_id'])
    except ValueError as e:
        logging.error("Invalid team_id: %s", e)
        return jsonify({'error': 'Invalid team_id'}), 400

    # Use generate_password_hash for hashing the password
    hashed_password = generate_password_hash(data['password'])

    try:
        with open('users.json', 'r+') as f:
            users_data = json.load(f)

            new_user_id = max([user['id'] for user in users_data['users']], default=0) + 1
            new_user = {
                'id': new_user_id,
                'username': data['name'],
                'password': hashed_password,  # Store the hashed password
                'team_id': str(team_id),  # Ensure consistency in data type
                'role': 'user'  # Default role; adjust as necessary
            }
            users_data['users'].append(new_user)

            f.seek(0)
            json.dump(users_data, f, indent=4)
            f.truncate()
            logging.info("User created successfully: %s", new_user_id)  # Log success
    except Exception as e:
        logging.exception("Failed to update users.json: %s", e)
        return jsonify({'error': 'Failed to update users.json', 'exception': str(e)}), 500

    return jsonify({'message': 'User created successfully', 'user_id': new_user_id}), 200




    
@staticmethod
def get(user_id):
    with open('users.json') as f:
        users_data = json.load(f).get('users', [])
        for user_data in users_data:
            if str(user_data.get('id')) == str(user_id):
                return User(user_data)  # Correctly returns a User object
    return None  
    
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        # Open and read the users.json file
        with open('users.json', 'r') as f:
            data = json.load(f)
        
        # Filter out the user with the given user_id
        updated_users = [user for user in data['users'] if user['id'] != user_id]
        
        # Update the 'users' list in the data dictionary
        data['users'] = updated_users
        
        # Write the updated data back to users.json
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500

def get_user(user_id):
    user = get_user_details(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/get_user_details/<int:user_id>')
def get_user_details(user_id):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


def update_user(user_id, new_name, new_team_id):
    with open('teams.json', 'r+') as f:
        data = json.load(f)
        for user in data['users']:
            if user['id'] == user_id:
                user['name'] = new_name
                user['team_id'] = new_team_id
                f.seek(0)  # Reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()  # Remove remaining part of the old content
                return True
    return False
        

@app.route('/update_user_details', methods=['POST'])
def update_user_details():
    data = request.get_json()
    user_id = data.get('id')
    new_name = data.get('name')
    new_team_id = data.get('team_id')

    # Load users, find the specific user, and update their details
    try:
        with open('users.json', 'r+') as file:
            users_data = json.load(file)
            for user in users_data.get('users', []):
                if user['id'] == user_id:
                    user['username'] = new_name  # Assuming 'username' field
                    user['team_id'] = new_team_id
                    break

            file.seek(0)
            json.dump(users_data, file, indent=4)
            file.truncate()

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
def is_user_in_team(username, team_name):
    # Placeholder for your logic to check if a user belongs to a specified team
    # This might involve querying a database
    # For demonstration, let's say it returns True if the user is in the team, False otherwise
    user_team = get_user_team(username)  # Assuming this function returns the team name the user belongs to
    return user_team == team_name
        
