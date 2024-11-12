import logging
from typing import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.utils.password_manager import PasswordManager
from src.business.utils.validation import Validation
from src.data_access.user_repository import UserRepository
from src.database.models.user import User


class UserManager:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.validator = Validation()
        self.current_user = None

    def register(self, username: str, password: str,
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
            user = self.user_repository.create_user(username, hashed_password, email)

            return True, user

        except SecurityException as e:
            logging.error(f"Security error during registration: {str(e)}")
            return False, User()
        except Exception as e:
            logging.error(f"Error during registration: {str(e)}")
            return False, User()

    def login(self, email: str, password: str) -> Tuple[bool, User]:
        user = self.user_repository.get_user_by_email(email)

        if user and PasswordManager.verify_password(password, user.password_hash):
            self.current_user = user
            return True, user
        return False, User()

    def update_user(self, user_dto: User) -> User:
        return self.user_repository.update_user(user_dto)
