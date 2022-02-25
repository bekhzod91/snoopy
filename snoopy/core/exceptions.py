class SnoopyException(Exception):
    code: str
    message: str


class Unauthorized(Exception):
    code = "unauthorized"
    message = "Unauthorized."
