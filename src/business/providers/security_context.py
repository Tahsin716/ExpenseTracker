from src.data_access.models.user import User


class SecurityContext:
    current_user : User | None = None