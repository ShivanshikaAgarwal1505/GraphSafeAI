from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from shared.database.dependency import (
    get_db,
)

from shared.database.current_user import (
    get_current_user,
)

from shared.database.models.user import (
    User,
)

from shared.database.models.favorite_location import (
    FavoriteLocation,
)

from shared.schemas.favorite_schema import (
    FavoriteCreateRequest,
    FavoriteResponse,
)

router = APIRouter(
    prefix="/api/v1/favorites",
    tags=["Favorites"],
)


@router.get(
    "",
    response_model=list[FavoriteResponse],
)
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):
    return (
        db.query(
            FavoriteLocation,
        )
        .filter(
            FavoriteLocation.user_id
            == current_user.id
        )
        .all()
    )


@router.post(
    "",
    response_model=FavoriteResponse,
)
def create_favorite(
    request: FavoriteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):
    favorite = FavoriteLocation(
        user_id=current_user.id,
        label=request.label,
        latitude=request.latitude,
        longitude=request.longitude,
    )

    db.add(favorite)

    db.commit()

    db.refresh(favorite)

    return favorite


@router.delete(
    "/{favorite_id}",
)
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):
    favorite = (
        db.query(
            FavoriteLocation,
        )
        .filter(
            FavoriteLocation.id
            == favorite_id,
            FavoriteLocation.user_id
            == current_user.id,
        )
        .first()
    )

    if favorite:
        db.delete(favorite)
        db.commit()

    return {
        "success": True,
    }