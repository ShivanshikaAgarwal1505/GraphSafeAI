from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from shared.database.dependency import (
    get_db,
)

from shared.security.jwt import (
    decode_access_token,
)

from services.authentication.infrastructure.user_repository import (
    UserRepository,
)

security = HTTPBearer()

repository = UserRepository()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    db: Session = Depends(
        get_db,
    ),
):

    token = credentials.credentials

    payload = decode_access_token(
        token,
    )

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
        )

    user_id = int(
        payload["sub"]
    )

    user = repository.get_by_id(
        db,
        user_id,
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found.",
        )

    return user