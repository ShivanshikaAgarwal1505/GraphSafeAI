import heapq

from services.routing_engine.infrastructure.graph_repository import (
    GraphRepository
)

from shared.config.routing_config import (
    CURRENT_RISK_WEIGHT,
    PREDICTED_RISK_WEIGHT,
    MAX_SAFETY_SCORE,
    ROUTING_MODES
)


class RoutingService:

    DEFAULT_MODE = "balanced"

    def __init__(
        self
    ):

        self.repository = (
            GraphRepository()
        )

    def safest_route(
        self,
        db,
        source_region_id: int,
        destination_region_id: int,
        mode: str = DEFAULT_MODE
    ):

        if mode not in ROUTING_MODES:

            mode = self.DEFAULT_MODE

        risk_weight = (
            ROUTING_MODES[mode]
            ["risk_weight"]
        )

        distance_weight = (
            ROUTING_MODES[mode]
            ["distance_weight"]
        )

        graph = (
            self.repository
            .build_graph(db)
        )

        risk_map = (
            self.repository
            .risk_map(db)
        )

        prediction_map = (
            self.repository
            .prediction_map(db)
        )

        queue = []

        heapq.heappush(
            queue,
            (
                0.0,
                source_region_id,
                [source_region_id]
            )
        )

        visited = set()

        while queue:

            cost, node, path = (
                heapq.heappop(
                    queue
                )
            )

            if node in visited:

                continue

            visited.add(node)

            if node == destination_region_id:

                route_risks = [
                    risk_map.get(
                        region,
                        0.0
                    )
                    for region in path
                ]

                average_risk = (
                    sum(route_risks)
                    / len(route_risks)
                )

                max_risk_region = max(
                    path,
                    key=lambda r:
                    risk_map.get(
                        r,
                        0.0
                    )
                )

                max_risk = risk_map.get(
                    max_risk_region,
                    0.0
                )

                route_safety_score = (
                    MAX_SAFETY_SCORE
                    - average_risk
                )

                high_risk_regions = [

                    region

                    for region in path

                    if risk_map.get(
                        region,
                        0.0
                    ) > average_risk
                ]

                return {

                    "source_region_id":
                        source_region_id,

                    "destination_region_id":
                        destination_region_id,

                    "routing_mode":
                        mode,

                    "route":
                        path,

                    "total_cost":
                        round(
                            cost,
                            4
                        ),

                    "average_risk":
                        round(
                            average_risk,
                            4
                        ),

                    "max_risk":
                        round(
                            max_risk,
                            4
                        ),

                    "route_safety_score":
                        round(
                            route_safety_score,
                            4
                        ),

                    "region_count":
                        len(path),

                    "explanation": {

                        "highest_risk_region":
                            max_risk_region,

                        "highest_risk_score":
                            round(
                                max_risk,
                                4
                            ),

                        "average_route_risk":
                            round(
                                average_risk,
                                4
                            ),

                        "high_risk_regions":
                            high_risk_regions,

                        "high_risk_region_count":
                            len(
                                high_risk_regions
                            ),

                        "risk_weight":
                            risk_weight,

                        "distance_weight":
                            distance_weight,

                        "current_risk_weight":
                            CURRENT_RISK_WEIGHT,

                        "predicted_risk_weight":
                            PREDICTED_RISK_WEIGHT
                    }
                }

            for neighbor in graph.get(
                node,
                []
            ):

                if neighbor in visited:

                    continue

                current_risk = (
                    risk_map.get(
                        neighbor,
                        0.0
                    )
                )

                predicted_risk = (
                    prediction_map.get(
                        neighbor,
                        current_risk
                    )
                )

                combined_risk = (

                    current_risk
                    *
                    CURRENT_RISK_WEIGHT

                    +

                    predicted_risk
                    *
                    PREDICTED_RISK_WEIGHT
                )

                edge_cost = (

                    combined_risk
                    *
                    risk_weight

                    +

                    distance_weight
                )

                heapq.heappush(

                    queue,

                    (
                        cost +
                        edge_cost,

                        neighbor,

                        path +
                        [neighbor]
                    )
                )

        return None