import logging
from typing import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.providers.roles import Roles
from src.business.providers.security_context import SecurityContext
from src.business.utils.password_manager import PasswordManager
from src.business.utils.validation import Validation
from src.data_access.user_repository import UserRepository
from src.data_access.models.user import User


class UserManager:
    def __init__(self):
        self.user_repository = UserRepository()
        self.validator = Validation()

    def register(self, first_name: str, last_name: str, password: str,
                      email: str, is_admin : bool) -> Tuple[bool, str, User]:
        try:
            if not first_name or len(first_name) == 0:
                raise SecurityException("First Name cannot be empty")

            if not last_name or len(last_name) == 0:
                raise SecurityException("Last Name cannot be empty")

            if not self.validator.validate_email(email):
                raise SecurityException("Invalid email format")

            if self.user_repository.email_exists(email):
                raise SecurityException("Email already exists in the system")

            if not self.validator.validate_password(password):
                raise SecurityException(
                    "Password must be at least 8 characters long and contain "
                    "uppercase, lowercase, numbers, and special characters"
                )

            first_name = self.validator.sanitize_input(first_name)
            last_name = self.validator.sanitize_input(last_name)
            email = self.validator.sanitize_input(email)

            hashed_password = PasswordManager.hash_password(password)
            user = self.user_repository.create_user(first_name, last_name, hashed_password, email, is_admin)

            SecurityContext.current_user = user
            return True, "", user

        except SecurityException as e:
            logging.error(f"Security error during registration: {str(e)}")
            return False, str(e) ,User()
        except Exception as e:
            logging.error(f"Error during registration: {str(e)}")
            return False, str(e), User()

    def login(self, email: str, password: str) -> Tuple[bool,User]:
        user = self.user_repository.get_user_by_email(email)

        if user and PasswordManager.verify_password(password, user.password_hash):
            SecurityContext.current_user = user
            return True, user
        return False, User()

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def update_user(self, user_id : int, first_name : str, last_name : str, email : str)  -> Tuple[bool, str, User]:
        try:
            if not first_name or len(first_name) == 0:
                raise SecurityException("First Name cannot be empty")

            if not last_name or len(last_name) == 0:
                raise SecurityException("Last Name cannot be empty")

            if not self.validator.validate_email(email):
                raise SecurityException("Invalid email format")

            return self.user_repository.update_user(user_id, first_name, last_name, email)

        except SecurityException as e:
            logging.error(f"Security exception during user update: {str(e)}")
            return False, str(e), User()

        except Exception as e:
            logging.error(f"Error during user update: {str(e)}")
            return False, str(e), User()


    def delete_user(self, user_id : int) -> Tuple[bool, str]:
        try:
            if SecurityContext.current_user.user_id == user_id:
                raise SecurityException("Cannot delete logged in user")

            user = self.user_repository.get_user_by_id(user_id)

            if SecurityContext.current_user.role == Roles.USER and user.role == Roles.ADMIN:
                raise  SecurityException("User does not have permission to delete an admin")

            self.user_repository.delete_user(user_id)
            return True, ""

        except SecurityException as e:
            logging.error(f"Security exception during user delete: {str(e)}")
            return False, str(e)

        except Exception as e:
            logging.error(f"Error during user delete: {str(e)}")
            return False, str(e)