import secrets
import datetime
from snoopy.core import db

from ..models.session import Session
from ..models.user import User
from ..exceptions import InvalidCredential

from schemas import SignInRequestDTO, SignInResponseDTO


class SignInService(object):
    def __init__(self, data: "SignInRequestDTO", user_agent: str, remote_addr: str):
        self.data = data
        self.user_agent = user_agent
        self.remote_addr = remote_addr

    @staticmethod
    def get_user_by_credential(username: str, password: str):
        user = User.query.filter_by(username=username).first()

        if not user or not user.password_verify(password.strip()):
            raise InvalidCredential

        return user

    @staticmethod
    def create_session(user: "User", device: str, remote_addr: str):
        session = Session(
            token=secrets.token_urlsafe(30),
            user_guid=user.guid,
            device=device,
            ip_address=remote_addr,
            last_activity=datetime.datetime.utcnow(),
            created_at=datetime.datetime.utcnow()
        )

        db.session.add(session)
        db.session.commit()

        return session.token

    def execute(self) -> "SignInResponseDTO":
        user = SignInService.get_user_by_credential(
            self.data.username, self.data.password
        )
        token = SignInService.create_session(
            user, self.user_agent, self.remote_addr
        )
        return SignInResponseDTO(token=token)
