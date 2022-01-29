from ..models.session import Session

from schemes import SignOutRequestDTO


class SignOutService(object):
    def __init__(self, data: "SignOutRequestDTO"):
        self.data = data

    @staticmethod
    def delete_session(token: str):
        Session.query.filter_by(token=token).delete()

    def execute(self):
        SignOutService.delete_session(self.data.token)
