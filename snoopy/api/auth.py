from http import HTTPStatus
from flask import Response, request, g
from flask.blueprints import Blueprint

from snoopy.auth import is_authenticated
from snoopy.auth.services.sign_in import SignInService
from snoopy.auth.services.sign_out import SignOutService
from snoopy.auth.services.forgot_password import ForgotPasswordService
from snoopy.auth.services.forgot_password_confirm import ForgotPasswordConfirmService

from schemas import (
    SignInRequestDTO, SignOutRequestDTO,
    ForgotPasswordRequestDTO, ForgotPasswordConfirmRequestDTO
)


auth_blueprint = Blueprint('auth', __name__, url_prefix="/api/v1/auth/")


@auth_blueprint.post("/sign-in/")
def sign_in():
    user_agent = str(request.user_agent)
    remote_addr = str(request.remote_addr)

    req_dto = SignInRequestDTO(**request.json)
    res_dto = SignInService(req_dto, user_agent, remote_addr).execute()

    return Response(
        status=HTTPStatus.CREATED,
        response=res_dto.json(),
        content_type="application/json"
    )


@auth_blueprint.post("/sign-out/")
@is_authenticated
def sing_out():
    req_dto = SignOutRequestDTO(token=g.session.token)

    SignOutService(req_dto).execute()

    return Response(
        status=HTTPStatus.NO_CONTENT,
        content_type="application/json"
    )


@auth_blueprint.post("/forgot-password/")
def forgot_password():
    req_dto = ForgotPasswordRequestDTO(**request.json)

    ForgotPasswordService(req_dto).execute()

    return Response(
        status=HTTPStatus.NO_CONTENT,
        content_type="application/json"
    )


@auth_blueprint.post("/forgot-password/confirm/")
def forgot_password_confirm():
    req_dto = ForgotPasswordConfirmRequestDTO(**request.json)
    ForgotPasswordConfirmService(req_dto).execute()

    return Response(
        status=HTTPStatus.NO_CONTENT,
        content_type="application/json"
    )
