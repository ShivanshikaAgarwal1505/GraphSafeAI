from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from shared.database.session import get_db

from services.navigation_engine.application.nearest_node_service import (
    NearestNodeService
) 

from services.navigation_engine.application.navigation_service import (
    NavigationService
)

from shared.config.navigation_profiles import (
    NAVIGATION_PROFILES
)
from shared.database.models.region import Region

router = APIRouter(
    prefix="/api/v1/navigation",
    tags=["Navigation"]
)


@router.get(
    "/nearest-node"
)
def nearest_node(
    latitude: float,
    longitude: float
):

    return (
        NearestNodeService()
        .find_nearest_node(
            latitude,
            longitude
        )
    )
    
@router.get("/route")
def route(
    source_lat: float,
    source_lon: float,
    destination_lat: float,
    destination_lon: float,
    profile: str = "driving_balanced",
    db: Session = Depends(get_db)
):

    return (
        NavigationService()
        .route(
            db=db,
            source_lat=source_lat,
            source_lon=source_lon,
            destination_lat=destination_lat,
            destination_lon=destination_lon,
            profile=profile
        )
    )
    
@router.get("/search")
def search_locations(
    q: str,
    db: Session = Depends(get_db),
):
    results = (
        db.query(Region)
        .filter(
            Region.region_name.ilike(
                f"%{q}%"
            )
        )
        .limit(20)
        .all()
    )

    return [
        {
            "name": region.region_name,
            "latitude": region.centroid_lat,
            "longitude": region.centroid_lon,
        }
        for region in results
    ]
    
@router.get("/profiles")
def profiles():

    return NAVIGATION_PROFILES