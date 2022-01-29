import typing
from flask import request, g

from .models.session import Session
from .exceptions import InvalidToken, InvalidTokenType, Unauthorized


def check_authorization(authorization: str, remote_addr: str) -> "Session":
    type_, token = authorization.split(" ")

    if not type_ or not token:
        raise InvalidToken

    if type_ != "Token":
        raise InvalidTokenType

    session = Session.get_session_by_token(token)
    session.update_last_active(remote_addr)

    if not session:
        raise Unauthorized

    return session


def is_authenticated(func: typing.Callable) -> typing.Callable:
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        session = check_authorization(header, request.remote_addr)

        setattr(g, "user", session.user)
        setattr(g, "session", session)

        return func(*args, **kwargs)

    return wrapper
