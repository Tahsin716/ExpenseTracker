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
            salt_bytes = salt.to_bytes((salt.bit_length() + 7) // 8, byteorder='big')
            password_hash = hashlib.sha256(salt_bytes + password.encode()).hexdigest()

            return password_hash
        except Exception as e:
            logging.error(f"Error hashing password: {str(e)}")
            raise SecurityException("Error processing password")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            salt = Config.PASSWORD_SALT
            salt_bytes = salt.to_bytes((salt.bit_length() + 7) // 8, byteorder='big')
            return hashlib.sha256(salt_bytes + password.encode()).hexdigest() == hashed_password
        except Exception as e:
            logging.error(f"Error verifying password: {str(e)}")
            return False