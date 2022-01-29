from snoopy.core import SnoopyException


class InvalidCredential(SnoopyException):
    code = "invalid_credential"
    message = "Invalid credential. Check your username and password!"


class EmailAlreadyExists(SnoopyException):
    code = "email_already_exists"
    message = "This email already exists. Use forgot password!"


class InvalidToken(SnoopyException):
    code = "invalid_token"
    message = "Invalid authorization header, provide token."


class InvalidTokenType(SnoopyException):
    code = "invalid_token_type"
    message = (
        "Invalid authorization header. "
        "Use correct version, example \"Authorization: Token *******\"."
    )


class Unauthorized(SnoopyException):
    code = "unauthorized"
    message = "Unauthorized."

