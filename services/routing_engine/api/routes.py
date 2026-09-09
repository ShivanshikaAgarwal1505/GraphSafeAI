from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from shared.database.session import (
    get_db
)

from services.routing_engine.application.routing_service import (
    RoutingService
)

router = APIRouter(
    prefix="/api/v1/routing",
    tags=["Routing"]
)


@router.get(
    "/safe-route"
)
def safe_route(
    source_region_id: int,
    destination_region_id: int,
    mode: str = "balanced",
    db=Depends(
        get_db
    )
):

    route = (
        RoutingService()
        .safest_route(
            db,
            source_region_id,
            destination_region_id,
            mode
        )
    )

    if route is None:

        raise HTTPException(
            status_code=404,
            detail="Route not found"
        )

    return route