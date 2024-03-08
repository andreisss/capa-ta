from flask_login import UserMixin
import json

class User(UserMixin):
    def __init__(self, user_data):
        if not isinstance(user_data, dict):
            raise ValueError("Invalid user data format. Expected dictionary.")
        
        self.id = str(user_data.get('id'))  # Ensuring id is always a string
        self.username = user_data.get('username')
        self.password = user_data.get('password')
        self.team_id = str(user_data.get('team_id'))  # Re-adding team_id, ensure it's in your JSON if you use it
        self.role = user_data.get('role')

    @staticmethod
    def get(user_id):
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f).get('users', [])
        except Exception as e:
            raise IOError(f"Error reading users.json: {e}")
        
        for user_data in users_data:
            if str(user_data.get('id')) == str(user_id):
                return User(user_data)
        return None

    @staticmethod
    def get_by_username(username):
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f).get('users', [])
        except Exception as e:
            raise IOError(f"Error reading users.json: {e}")
        
        for user_data in users_data:
            if user_data.get('username') == username:
                return User(user_data)
        return None

