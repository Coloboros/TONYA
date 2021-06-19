from re import L
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.operators import is_
from sqlalchemy import update
from .tables import *
from .init_post import Session

def check_phone(phone):
    return len(''.join(c for c in phone if c.isdigit())) == 11


class DataBase:
    def __init__(self):
        self.session = Session()

    def add_user(self, id, name):
        is_exist = self.session.query(User.id).\
                    filter(User.id == id).all() != []
        if is_exist:
            return False

        user = User(id, name)
        self.session.add(user)
        self.session.commit()

        return True

    def get_users(self):
        return self.session.query(User).all()

    def get_user(self, user_id) -> User:
        finded_users = self.session.query(User).\
                    filter(User.id == user_id).all()
        if finded_users != []:
            return finded_users[0]
        else:
            return None

    def update_user_phone(self, user_id, user_phone):
        if not check_phone(user_phone):
            return False

        user = self.session.query(User).filter_by(id=user_id).first()
        user.phone = user_phone
        self.session.commit()
        return True

__all__ = ['DataBase']
