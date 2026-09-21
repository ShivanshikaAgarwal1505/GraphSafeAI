from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from shared.database.dependency import (
    get_db,
)

from shared.schemas.auth_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    LoginResponse,
    UserResponse,
)

from services.authentication.application.auth_service import (
    AuthService,
)

from shared.database.current_user import (
    get_current_user,
)
from shared.database.models.user import (
    User,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

service = AuthService()


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
):

    try:

        return service.register(
            db=db,
            name=request.name,
            email=request.email,
            password=request.password,
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):

    try:

        result = service.login(
            db=db,
            email=request.email,
            password=request.password,
        )

        return result

    except ValueError as ex:

        raise HTTPException(
            status_code=401,
            detail=str(ex),
        )
        
@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(
        get_current_user,
    ),
):

    return current_user