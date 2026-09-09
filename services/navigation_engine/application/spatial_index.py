from scipy.spatial import KDTree

from services.navigation_engine.infrastructure.navigation_repository import (
    NavigationRepository
)


class SpatialIndex:

    _tree = None

    _nodes = None

    @classmethod
    def build(
        cls
    ):

        if cls._tree is not None:

            return

        repository = (
            NavigationRepository()
        )

        nodes = (
            repository
            .nodes()
        )

        coordinates = list(
            zip(
                nodes["latitude"],
                nodes["longitude"]
            )
        )

        cls._tree = KDTree(
            coordinates
        )

        cls._nodes = nodes

        print(
            "KDTree built"
        )

    @classmethod
    def nearest(
        cls,
        latitude: float,
        longitude: float
    ):

        cls.build()

        _, index = (
            cls._tree.query(
                (
                    latitude,
                    longitude
                )
            )
        )

        row = (
            cls._nodes
            .iloc[index]
        )

        return {

            "node_id":
                int(
                    row["node_id"]
                ),

            "latitude":
                float(
                    row["latitude"]
                ),

            "longitude":
                float(
                    row["longitude"]
                )
        }