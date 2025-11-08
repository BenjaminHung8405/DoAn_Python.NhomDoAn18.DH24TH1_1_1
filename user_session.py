"""
User Session Manager
Manages user session information in memory instead of using local files
"""

class UserSession:
    _instance = None
    _current_user = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_user(cls, user_data):
        """Set the current logged in user"""
        cls._current_user = user_data

    @classmethod
    def get_user(cls):
        """Get the current logged in user"""
        return cls._current_user

    @classmethod
    def clear_user(cls):
        """Clear the current user session (logout)"""
        cls._current_user = None

    @classmethod
    def is_logged_in(cls):
        """Check if user is currently logged in"""
        return cls._current_user is not None

    @classmethod
    def get_user_id(cls):
        """Get the current user's ID"""
        if cls._current_user and 'uid' in cls._current_user:
            return cls._current_user['uid']
        return None