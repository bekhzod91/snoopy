from sqlalchemy.dialects.postgresql import UUID

from snoopy.core import db
from ..utils.security import check_password, make_password


class User(db.Model):
    __tablename__ = 'auth_user'

    guid = db.Column(UUID(), primary_key=True)
    username = db.Column(db.String(length=255), nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def password_verify(self, password):
        return check_password(password, self.password)

    def set_password(self, password):
        self.password = make_password(password)
