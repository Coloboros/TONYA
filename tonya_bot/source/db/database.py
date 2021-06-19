from . import User

def check_phone(phone):
    return len(''.join(c for c in phone if c.isdigit())) == 11


class DataBase:
    def __init__(self):
        pass

    def add_user(self, id, name):
        pass

    def get_users(self):
        pass

    def get_user(self, user_id) -> User:
        pass

    def update_user_phone(self, user_id, user_phone):
        pass

__all__ = ['DataBase']
