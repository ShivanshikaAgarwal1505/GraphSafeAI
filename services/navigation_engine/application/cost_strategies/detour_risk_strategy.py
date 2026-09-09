from shared.config.routing_config import (
    CURRENT_RISK_WEIGHT,
    PREDICTED_RISK_WEIGHT
)

from shared.providers.node_region_provider import (
    NodeRegionProvider
)


class DetourRiskStrategy:

    def __init__(
        self,
        risk_map,
        prediction_map,
        profile
    ):

        self.risk_map = risk_map

        self.prediction_map = prediction_map

        self.profile = profile

    def get_risk(
        self,
        node_id: int
    ):

        region_id = (
            NodeRegionProvider
            .get_region(
                node_id
            )
        )

        if region_id is None:
            return 0.0

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

        return (

            current_risk
            * CURRENT_RISK_WEIGHT

            +

            predicted_risk
            * PREDICTED_RISK_WEIGHT
        )

    def cost(
        self,
        node_id,
        distance_km
    ):

        risk = (
            self.get_risk(
                node_id
            )
        )
        
        # risk = self.get_risk(node_id)

        # if risk > 0:
        #     print(
        #         f"Node={node_id}, Risk={risk}"
        #     )

        return (
            distance_km
            *
            (
                1.0 + risk
            )
        )
        
    # def get_risk(
    # self,
    # node_id: int
    # ):

    #     region_id = (
    #     NodeRegionProvider.get_region(
    #         node_id
    #     )
    #     )

    #     if region_id is None:
    #         return 0.0

    #     current_risk = (
    #     self.risk_map.get(
    #         region_id,
    #         0.0
    #     )
    #     )

    #     predicted_risk = (
    #     self.prediction_map.get(
    #         region_id,
    #         current_risk
    #     )
    #     )

    #     combined_risk = (
    #     current_risk
    #     * CURRENT_RISK_WEIGHT
    #     +
    #     predicted_risk
    #     * PREDICTED_RISK_WEIGHT
    #     )

    #     return combined_risk