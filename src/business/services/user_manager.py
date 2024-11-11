import logging
from typing import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.utils.password_manager import PasswordManager
from src.business.utils.validation import Validation
from src.data_access.data_access import DataAccess
from src.database.models.user import User


class UserManager:
    def __init__(self, data_access: DataAccess):
        self.data_access = data_access
        self.validator = Validation()
        self.current_user = None

    def register_user(self, username: str, password: str,
                      email: str) -> Tuple[bool, User]:
        try:
            if not self.validator.validate_username(username):
                raise SecurityException("Invalid username format")

            if not self.validator.validate_email(email):
                raise SecurityException("Invalid email format")

            if not self.validator.validate_password(password):
                raise SecurityException(
                    "Password must be at least 8 characters long and contain "
                    "uppercase, lowercase, numbers, and special characters"
                )

            username = self.validator.sanitize_input(username)
            email = self.validator.sanitize_input(email)

            hashed_password = PasswordManager.hash_password(password)
            user = self.data_access.create_user(username, hashed_password, email)

            return True, user

        except SecurityException as e:
            logging.error(f"Security error during registration: {str(e)}")
            return False, User()
        except Exception as e:
            logging.error(f"Error during registration: {str(e)}")
            return False, User()

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, User]:
        user = self.data_access.get_user_by_username(username)

        if user and PasswordManager.verify_password(password, user.password_hash):
            self.current_user = user
            return True, user
        return False, User()