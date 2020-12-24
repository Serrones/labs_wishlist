from typing import Union

from app.models import User


def get_user_by_username(username: str) -> Union[User, None]:
    try:
        return User.query.filter(User.username == username).one()
    except Exception:
        return None
