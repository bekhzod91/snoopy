from datetime import datetime

from snoopy.core import db
from snoopy.auth.models.user import User
from schemas import ForgotPasswordConfirmRequestDTO, ForgotPasswordConfirmResponseDTO

from ..exceptions import InvalidForgotPasswordToken
from ..exceptions import NewPasswordIsWeek


MIN_PASSWORD_LENGTH = 8


class ForgotPasswordConfirmService(object):
    def __init__(self, data: "ForgotPasswordConfirmRequestDTO"):
        self.data = data

    @staticmethod
    def get_user_by_token(token: str):
        user = User.query.filter_by(forgot_password_token=token).first()

        if not user:
            raise InvalidForgotPasswordToken

        if user.forgot_password_expire < datetime.utcnow():
            user.forgot_password_token = None
            user.forgot_password_expire = None
            db.session.commit()

            raise InvalidForgotPasswordToken

        return user

    @staticmethod
    def change_password(user: "User", new_password: str):
        if len(new_password) < MIN_PASSWORD_LENGTH:
            raise NewPasswordIsWeek

        user.set_password(new_password.strip())
        user.forgot_password_token = None
        user.forgot_password_expire = None
        db.session.commit()

    def execute(self) -> "ForgotPasswordConfirmResponseDTO":
        user = ForgotPasswordConfirmService.get_user_by_token(self.data.token)
        ForgotPasswordConfirmService.change_password(user, self.data.new_password)
        return ForgotPasswordConfirmResponseDTO()
