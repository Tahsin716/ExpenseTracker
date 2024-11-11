import hashlib
import logging

from src.business.exception.security_exception import SecurityException
from src.business.utils.config import Config


class PasswordManager:

    @staticmethod
    def hash_password(password: str) -> str:
        if not password:
            raise SecurityException("Password cannot be empty")

        try:
            salt = Config.PASSWORD_SALT
            password_hash = hashlib.sha256(salt + password.encode()).hexdigest()

            return password_hash
        except Exception as e:
            logging.error(f"Error hashing password: {str(e)}")
            raise SecurityException("Error processing password")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            salt = Config.PASSWORD_SALT
            return hashlib.sha256(salt + password.encode()).hexdigest() == hashed_password
        except Exception as e:
            logging.error(f"Error verifying password: {str(e)}")
            return False