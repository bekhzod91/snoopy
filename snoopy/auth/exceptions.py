from snoopy.core import SnoopyException


class InvalidCredential(SnoopyException):
    code = "invalid_credential"
    message = "Invalid credential. Check your username and password!"


class EmailAlreadyExists(SnoopyException):
    code = "email_already_exists"
    message = "This email already exists. Use forgot password!"


class InvalidEmailAddress(SnoopyException):
    code = "invalid_email_address"
    message = "Invalid email address. Check your detail!"


class InvalidToken(SnoopyException):
    code = "invalid_token"
    message = "Invalid authorization header, provide token."


class InvalidTokenType(SnoopyException):
    code = "invalid_token_type"
    message = (
        "Invalid authorization header. "
        "Use correct version, example \"Authorization: Token *******\"."
    )


class InvalidForgotPasswordToken(SnoopyException):
    code = "invalid_forgot_password_token"
    message = (
        "Invalid forgot password token."
    )


class NewPasswordIsWeek(SnoopyException):
    code = "new_password_is_week"
    message = (
        "New password is week. "
        "Password should contain 8 characters!"
    )
