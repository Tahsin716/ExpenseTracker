import logging
import datetime

from typing_extensions import Tuple

from src.business.exception.security_exception import SecurityException
from src.business.providers.roles import Roles
from src.business.providers.security_context import SecurityContext
from src.data_access.data_access import DataAccess
from src.data_access.models.user import User


class UserRepository(DataAccess):

    def __init__(self):
        super().__init__()

    def create_user(self, first_name : str, last_name : str, password_hash : str, email : str, is_admin : bool) -> User:
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                password_hash=password_hash,
                email=email,
                role= Roles.ADMIN if is_admin else Roles.USER
            )
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def update_user(self, user_id : int, first_name : str, last_name : str, email : str) -> Tuple[bool, str, User]:
        try:
            user = self.session.query(User).filter_by(user_id=user_id).update({'email': email, 'first_name': first_name, 'last_name': last_name, 'updated_at': datetime.datetime.now(datetime.timezone.utc)})
            self.session.commit()
            return True, "", user
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_user(self, user_id: str) -> bool:
        if not SecurityContext.current_user.role == 'admin':
            SecurityException("User does not have permission to delete user")

        response = self.session.query(User).filter_by(user_id=user_id).first()

        if not response:
            logging.log("No user found with given user_id")
            return False

        try:
            self.session.query(User).filter_by(user_id=user_id).delete(synchronize_session=False)
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_users(self) -> list[User]:
        self.session.expire_all()
        return self.session.query(User).all()

    def get_user_by_email(self, email : str) -> User:
        return self.session.query(User).filter_by(email=email).first()
