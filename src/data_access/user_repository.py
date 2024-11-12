from datetime import datetime

from src.business.utils.password_manager import PasswordManager
from src.data_access.data_access import DataAccess
from src.database.models.user import User


class UserRepository(DataAccess):

    def __init__(self):
        super().__init__()

    def create_user(self, first_name, last_name, password_hash, email) -> User:
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                password_hash=password_hash,
                email=email
            )
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def update_user(self, user_dto : User) -> User:
        try:
            user = self.session.query(User).filter_by(user_id=user_dto.user_id).update({'email': user_dto.email, 'first_name': user_dto.first_name, 'last_name': user_dto.last_name, 'updated_at': datetime.utcnow()})
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()
