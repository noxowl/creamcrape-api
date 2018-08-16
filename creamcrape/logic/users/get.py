from flask import current_app, g

from creamcrape.db.db import session, rs
from .data import AuthorizedUser


def get_user(request):
    # user_cache = rs.get('cache:user:{0}'.format)
    user_cache = None
    if user_cache:
        user = None
    else:
        from .create import create_instant_user
        user = create_instant_user(request)
    return user


def get_authorized_user(token: str) -> AuthorizedUser or None:
    user = session.query(AuthorizedUser).filter_by(token).one_or_none()
    return user
