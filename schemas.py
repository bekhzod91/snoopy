# generated by datamodel-codegen:
#   filename:  swagger.json
#   timestamp: 2022-02-23T18:57:59+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class SignInResponseDTO(BaseModel):
    token: str = Field(..., description='Authorization token.')


class ErrorDTO(BaseModel):
    code: str = Field(..., description="The person's username.")
    message: str = Field(..., description="The person's password.")


class SignInRequestDTO(BaseModel):
    username: str = Field(..., description="The person's username.", example='admin')
    password: str = Field(..., description="The person's password.", example='Test1234')


class SignOutResponseDTO(BaseModel):
    pass


class SignOutRequestDTO(BaseModel):
    token: str = Field(..., description='Authrization token.')


class ForgotPasswordResponseDTO(BaseModel):
    pass


class ForgotPasswordRequestDTO(BaseModel):
    username: str = Field(..., description="The person's username.", example='admin')


class ForgotPasswordConfirmResponseDTO(BaseModel):
    pass


class ForgotPasswordConfirmRequestDTO(BaseModel):
    token: str = Field(..., description='The reset password token.', example='{token}')
    new_password: str = Field(..., description='New password.', example='Test1234')