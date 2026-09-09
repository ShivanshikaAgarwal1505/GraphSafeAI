from math import cos
from math import radians


class GeoUtils:

    KM_PER_DEGREE = 111.32

    @classmethod
    def fast_distance_km(
        cls,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:

        avg_lat = (
            lat1 + lat2
        ) / 2

        dx = (
            lon2 - lon1
        ) * cls.KM_PER_DEGREE * cos(
            radians(avg_lat)
        )

        dy = (
            lat2 - lat1
        ) * cls.KM_PER_DEGREE

        return (
            dx * dx + dy * dy
        ) ** 0.5