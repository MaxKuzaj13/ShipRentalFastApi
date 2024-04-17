from sqlalchemy.orm import Session
from typing import Optional

from models import User
from repositories.common import Repository


class UserRepository(Repository):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def get_user_by_identifier(db: Session, identifier: str):
        """
        Fetches a user by either username or email.

        :param db: Database session
        :type db: sqlalchemy.orm.Session
        :param identifier: Username or email of the user
        :type identifier: str
        :return: User object if found, otherwise None
        :rtype: Optional[User]
        """
        return db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()


user_repo = UserRepository()
