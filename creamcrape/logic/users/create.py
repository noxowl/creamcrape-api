from flask import current_app, g
from .data import User


def create_instant_user(request) -> User:
    username = ''
    email = ''
    remote_address = request.remote_addr
    if current_app.config['DEBUG']:
        payload = request.json
    else:
        payload = request.msgpack
    if payload:
        username = payload['username'] if 'username' in payload else ''
        email = payload['email'] if 'email' in payload else ''
    user = User()
    user.set(
        username=username,
        email=email
    )
    user.set_credential(remote_address)
    return user
