from src.database.models.user import User


class SecurityContext:
    current_user : User | None = None