import re
import secrets
import datetime
from datetime import timedelta

from flask import current_app as app
from flask import render_template
from flask_mail import Message

from snoopy.core import mail, db
from schemas import ForgotPasswordRequestDTO, ForgotPasswordResponseDTO

from ..models.user import User
from ..exceptions import InvalidEmailAddress


class ForgotPasswordService(object):
    def __init__(self, data: "ForgotPasswordRequestDTO"):
        self.data = data

    @staticmethod
    def send_email_to_user(user: "User"):
        msg = Message()
        msg.sender = "noreply@tillakhanov.com"
        msg.recipients = [user.username]
        msg.subject = "Forgot your password?"
        msg.html = render_template(
            "forgot-password.html",
            domain=app.config["APP_DOMAIN"],
            token=user.forgot_password_token,
        )
        mail.send(msg)

    @staticmethod
    def send_verify_link(username: str):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.match(pattern, username):
            raise InvalidEmailAddress

        user = User.query.filter_by(username=username).first()
        token = secrets.token_urlsafe(40)

        if user:
            user.forgot_password_token = token
            user.forgot_password_expire = datetime.datetime.utcnow() + timedelta(hours=2)
            db.session.commit()
            ForgotPasswordService.send_email_to_user(user)

    def execute(self) -> "ForgotPasswordResponseDTO":
        self.send_verify_link(self.data.username)
        return ForgotPasswordResponseDTO()
