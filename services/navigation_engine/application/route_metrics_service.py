from services.navigation_engine.application.geo_utils import (
    GeoUtils
)

from services.navigation_engine.application.node_lookup import (
    NodeLookup
)
from services.navigation_engine.application.graph_builder import (
    GraphBuilder
)

class RouteMetricsService:

    def summarize(
        self,
        route: list[int]
    ):

        if not route:
            return {}

        total_distance = 0.0

        for index in range(
            len(route) - 1
        ):

            current = (
                NodeLookup.get(
                    route[index]
                )
            )

            nxt = (
                NodeLookup.get(
                    route[index + 1]
                )
            )

            if (
                current is None
                or nxt is None
            ):
                continue

            total_distance += (
                GeoUtils.fast_distance_km(
                    current[0],
                    current[1],
                    nxt[0],
                    nxt[1]
                )
            )

        return {

            "distance_km":
                round(
                    total_distance,
                    3
                ),

            "hop_count":
                len(route)
        }

    def distance_km(
        self,
        route
    ):

        if not route:

            return 0.0

        graph = (
            GraphBuilder.build()
        )

        total = 0.0

        for i in range(
            len(route) - 1
        ):

            current = route[i]

            nxt = route[i + 1]

            for neighbor, distance in graph.get(
                current,
                []
            ):

                if neighbor == nxt:

                    total += distance

                    break

        return round(
            total,
            3
        )

    def summarize(
        self,
        route
    ):

        return {

            "distance_km":
                self.distance_km(
                    route
                ),

            "hop_count":
                len(route)
                if route
                else 0
        }