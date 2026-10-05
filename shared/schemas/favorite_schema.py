from pydantic import BaseModel


class FavoriteCreateRequest(
    BaseModel,
):
    label: str

    latitude: float

    longitude: float


class FavoriteResponse(
    BaseModel,
):
    id: int

    label: str

    latitude: float

    longitude: float

    class Config:
        from_attributes = True