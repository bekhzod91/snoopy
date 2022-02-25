import typing
import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import NoResultFound

from snoopy.core import db


class Session(db.Model):
    __tablename__ = 'auth_session'

    token = db.Column(db.String(length=255), unique=True, primary_key=True)
    user_guid = db.Column(UUID, db.ForeignKey("auth_user.guid"), nullable=False)
    user = db.relationship("User", backref=db.backref("auth_user", lazy=True))
    device = db.Column(db.String(length=1000), nullable=False)
    ip_address = db.Column(db.String(length=255), nullable=False)
    last_activity = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"<Session {self.token}>"

    @staticmethod
    def get_session_by_token(token: str) -> typing.Optional["Session"]:
        try:
            session = Session.query.filter_by(token=token).one()
            return session
        except NoResultFound:
            return None

    def set_last_active(self, ip_address):
        self.ip_address = ip_address
        self.last_activity = datetime.datetime.utcnow()
