from pydantic import BaseModel
from pydantic import Field

class UserRegisterRequest(
    BaseModel
):

    name: str

    email: str

    password: str = Field(
        min_length=8,
        max_length=72,
    )


class UserLoginRequest(
    BaseModel
):

    email: str

    password: str = Field(
        min_length=8,
        max_length=72,
    )


class UserResponse(
    BaseModel
):

    id: int

    name: str

    email: str

    reputation_score: int

    reports_submitted: int

    reports_verified: int

    class Config:
        from_attributes = True


class LoginResponse(
    BaseModel
):

    access_token: str

    user: UserResponse