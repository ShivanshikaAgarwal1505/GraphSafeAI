from pydantic import BaseModel


class RouteResponse(
    BaseModel
):

    source_region_id: int

    destination_region_id: int

    route: list[int]

    total_cost: float

    region_count: int