from shared.config.routing_config import (
    CURRENT_RISK_WEIGHT,
    PREDICTED_RISK_WEIGHT,
    ROUTING_MODES
)

from shared.providers.node_region_provider import (
    NodeRegionProvider
)


class NavigationCostService:

    def __init__(
        self,
        risk_map,
        prediction_map
    ):

        self.risk_map = risk_map

        self.prediction_map = (
            prediction_map
        )

    def edge_cost(
        self,
        node_id: int,
        distance_km: float,
        mode: str
    ):

        if mode not in ROUTING_MODES:

            mode = "balanced"

        region_id = (
            NodeRegionProvider
            .get_region(
                node_id
            )
        )

        current_risk = (
            self.risk_map.get(
                region_id,
                0.0
            )
        )

        predicted_risk = (
            self.prediction_map.get(
                region_id,
                current_risk
            )
        )

        combined_risk = (

            current_risk
            * CURRENT_RISK_WEIGHT

            +

            predicted_risk
            * PREDICTED_RISK_WEIGHT
        )

        risk_weight = (
            ROUTING_MODES[mode]
            ["risk_weight"]
        )

        distance_weight = (
            ROUTING_MODES[mode]
            ["distance_weight"]
        )
        
        adjusted_risk = (
            combined_risk
            * risk_weight
        )

        return (
            distance_km
            * distance_weight
            * (
                1.0 + adjusted_risk
            )
        )