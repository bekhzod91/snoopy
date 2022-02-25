from snoopy.core import db

from ..models.session import Session

from schemas import SignOutRequestDTO, SignOutResponseDTO


class SignOutService(object):
    def __init__(self, data: "SignOutRequestDTO"):
        self.data = data

    @staticmethod
    def delete_session(token: str):
        Session.query.filter_by(token=token).delete()
        db.session.commit()

    def execute(self) -> "SignOutResponseDTO":
        SignOutService.delete_session(self.data.token)

        return SignOutResponseDTO()
