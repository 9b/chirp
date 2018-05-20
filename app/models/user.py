"""Bare bones user account model."""
from werkzeug.security import check_password_hash


class User():

    """User class used in the login process."""

    def __init__(self, user):
        self.username = user.get('username')
        self.email = user.get('email')
        self.first_name = user.get('first_name')
        self.last_name = user.get('last_name')
        self.groups = user.get('groups')
        self.first_active = user.get('first_active')
        self.last_active = user.get('last_active')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        if 'admin' in self.groups:
            return True
        return False

    def get_id(self):
        return self.username

    def get_name(self):
        return self.first_name + " " + self.last_name

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
