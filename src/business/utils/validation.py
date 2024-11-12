import re
import html

from src.business.utils.config import Config


class Validation:


    @staticmethod
    def validate_email(email: str) -> bool:
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))

    """
    Validate password strength
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    @staticmethod
    def validate_password(password: str) -> bool:

        if len(password) < Config.MIN_PASSWORD_LENGTH:
            return False

        patterns = [
            r'[A-Z]',  # Uppercase letter
            r'[a-z]',  # Lowercase letter
            r'[0-9]',  # Number
            r'[!@#$%^&*(),.?":{}|<>]'  # Special character
        ]

        return all(bool(re.search(pattern, password)) for pattern in patterns)

    """Sanitize input to prevent XSS attacks"""
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        return html.escape(input_string.strip())