from services.navigation_engine.infrastructure.navigation_repository import (
    NavigationRepository
)


class NearestNodeService:

    def __init__(
        self
    ):

        self.repository = (
            NavigationRepository()
        )

    def find_nearest_node(
        self,
        latitude: float,
        longitude: float
    ):

        nodes = (
            self.repository
            .nodes()
        )

        nodes = nodes.copy()

        nodes[
            "distance"
        ] = (

            (
                nodes["latitude"]
                - latitude
            ) ** 2

            +

            (
                nodes["longitude"]
                - longitude
            ) ** 2

        )

        nearest = (
            nodes
            .sort_values(
                "distance"
            )
            .iloc[0]
        )

        return {

            "node_id":
                int(
                    nearest["node_id"]
                ),

            "latitude":
                float(
                    nearest["latitude"]
                ),

            "longitude":
                float(
                    nearest["longitude"]
                )
        }