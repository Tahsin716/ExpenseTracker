import logging

from src.data_access.data_access import DataAccess


class UserManager:
    def __init__(self, data_access: DataAccess):
        self.data_access = data_access
        self.current_user = None

    def register_user(self, username: str, password: str,
                      email: str) -> bool:
        try:
            if not self.validator.validate_username(username):
                raise SecurityError("Invalid username format")

            if not self.validator.validate_email(email):
                raise SecurityError("Invalid email format")

            if not self.validator.validate_password(password):
                raise SecurityError(
                    "Password must be at least 8 characters long and contain "
                    "uppercase, lowercase, numbers, and special characters"
                )

            username = self.validator.sanitize_input(username)
            email = self.validator.sanitize_input(email)

            hashed_password = password # TODO: Hash the password
            user = self.data_access.create_user(username, hashed_password, email)

            return True

        except SecurityError as e:
            logging.error(f"Security error during registration: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Error during registration: {str(e)}")
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.data_access.get_user_by_username(username)

        if user: # and verify_password(password, user.password_hash): TODO: password hash verification
            self.current_user = user
            return True
        return False