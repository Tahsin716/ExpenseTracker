import logging
import datetime
from tkinter.ttk import Treeview

from typing_extensions import Tuple
from sqlalchemy import Select

from src.business.providers.roles import Roles
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

    def delete_user(self, user_id: int):
        try:
            self.session.query(User).filter_by(user_id=user_id).delete(synchronize_session=False)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_users(self) -> list[User]:
        self.session.expire_all()
        return self.session.query(User).all()

    def get_user_by_email(self, email : str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id : int) -> User:
        return self.session.query(User).filter_by(user_id=user_id).first()
