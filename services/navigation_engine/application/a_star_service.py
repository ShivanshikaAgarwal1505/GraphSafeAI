import heapq

from services.navigation_engine.application.geo_utils import (
    GeoUtils
)

from services.navigation_engine.application.graph_builder import (
    GraphBuilder
)

from services.navigation_engine.application.node_lookup import (
    NodeLookup
)


class AStarService:

    def __init__(
        self,
        strategy
    ):

        self.graph = (
            GraphBuilder.build()
        )

        self.strategy = strategy

    def heuristic(
        self,
        current_node: int,
        destination_node: int
    ) -> float:

        current = (
            NodeLookup.get(
                current_node
            )
        )

        destination = (
            NodeLookup.get(
                destination_node
            )
        )

        if (
            current is None
            or destination is None
        ):
            return 0.0

        return (
            GeoUtils.fast_distance_km(
                current[0],
                current[1],
                destination[0],
                destination[1]
            )
        )

    def find_path(
        self,
        source_node: int,
        destination_node: int,
        max_distance_km=None
    ):

        queue = []

        heapq.heappush(
            queue,
            (
                0.0,
                source_node
            )
        )

        #
        # Risk-adjusted optimization score
        #
        cost_score = {
            source_node: 0.0
        }

        #
        # Actual travelled distance
        #
        distance_score = {
            source_node: 0.0
        }

        parent = {}

        while queue:

            _, current = (
                heapq.heappop(
                    queue
                )
            )

            if current == destination_node:

                path = [current]

                while current in parent:

                    current = (
                        parent[current]
                    )

                    path.append(
                        current
                    )

                path.reverse()

                return path

            for neighbor, distance in self.graph.get(
                current,
                []
            ):

                #
                # Actual travelled distance
                #
                tentative_distance = (
                    distance_score[current]
                    + distance
                )

                #
                # Enforce detour constraint
                #
                if (
                    max_distance_km is not None
                    and
                    tentative_distance > max_distance_km
                ):
                    continue

                #
                # Risk-aware optimization cost
                #
                edge_cost = (
                    self.strategy.cost(
                        neighbor,
                        distance
                    )
                )

                tentative_cost = (
                    cost_score[current]
                    + edge_cost
                )

                if (
                    neighbor not in cost_score
                    or tentative_cost
                    < cost_score[neighbor]
                ):

                    cost_score[neighbor] = (
                        tentative_cost
                    )

                    distance_score[neighbor] = (
                        tentative_distance
                    )

                    parent[
                        neighbor
                    ] = current

                    f_score = (
                        tentative_cost
                        +
                        self.heuristic(
                            neighbor,
                            destination_node
                        )
                    )

                    heapq.heappush(
                        queue,
                        (
                            f_score,
                            neighbor
                        )
                    )

        return None