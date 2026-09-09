from services.navigation_engine.application.a_star_service import (
    AStarService
)

from services.navigation_engine.application.route_metrics_service import (
    RouteMetricsService
)

from services.navigation_engine.application.spatial_index import (
    SpatialIndex
)

from services.navigation_engine.application.cost_strategies.detour_risk_strategy import (
    DetourRiskStrategy
)

from services.navigation_engine.application.cost_strategies.distance_only_strategy import (
    DistanceOnlyStrategy
)

from shared.providers.risk_provider import (
    RiskProvider
)

from shared.providers.prediction_provider import (
    PredictionProvider
)

from shared.config.navigation_profiles import (
    NAVIGATION_PROFILES
)


class NavigationService:

    def route(
        self,
        db,
        source_lat: float,
        source_lon: float,
        destination_lat: float,
        destination_lon: float,
        profile: str = "walking_balanced"
    ):

        source_node = (
            SpatialIndex.nearest(
                source_lat,
                source_lon
            )
        )

        destination_node = (
            SpatialIndex.nearest(
                destination_lat,
                destination_lon
            )
        )

        metrics_service = (
            RouteMetricsService()
        )

        risk_map = (
            RiskProvider()
            .get_risk_map(db)
        )

        prediction_map = (
            PredictionProvider()
            .get_prediction_map(db)
        )

        #
        # Baseline shortest path
        #
        baseline_route = (
            AStarService(
                DistanceOnlyStrategy()
            )
            .find_path(
                source_node["node_id"],
                destination_node["node_id"]
            )
        )

        baseline_distance_km = (
            metrics_service
            .distance_km(
                baseline_route
            )
        )

        profile_config = (
            NAVIGATION_PROFILES[
                profile
            ]
        )

        max_distance_km = (
            baseline_distance_km
            *
            profile_config[
                "max_detour_ratio"
            ]
        )

        #
        # Floating-point tolerance
        #
        max_distance_km += 0.01

        #
        # Strategy selection
        #
        if profile.endswith(
            "fastest"
        ):

            strategy = (
                DistanceOnlyStrategy()
            )

        else:

            strategy = (
                DetourRiskStrategy(
                    risk_map,
                    prediction_map,
                    profile
                )
            )

        route = (
            AStarService(
                strategy
            )
            .find_path(
                source_node["node_id"],
                destination_node["node_id"],
                max_distance_km=max_distance_km
            )
        )

        if route is None:

            return {

                "profile":
                    profile,

                "baseline_distance_km":
                    round(
                        baseline_distance_km,
                        3
                    ),

                "max_allowed_distance_km":
                    round(
                        max_distance_km,
                        3
                    ),

                "source_node":
                    source_node["node_id"],

                "destination_node":
                    destination_node["node_id"],

                "route":
                    None,

                "route_length":
                    0,

                "metrics": {

                    "distance_km":
                        0,

                    "hop_count":
                        0
                },

                "risk_metrics": {

                    "average_risk":
                        0,

                    "max_risk":
                        0,

                    "risk_node_count":
                        0
                }
            }

        #
        # Risk metrics
        #
        risk_strategy = (
            DetourRiskStrategy(
                risk_map,
                prediction_map,
                profile
            )
        )

        route_risks = []

        for node_id in route:

            route_risks.append(
                risk_strategy.get_risk(
                    node_id
                )
            )

        avg_risk = (
            sum(route_risks)
            / len(route_risks)
        )

        max_risk = (
            max(route_risks)
        )

        risk_nodes = len(
            [
                risk
                for risk in route_risks
                if risk > 0
            ]
        )

        metrics = (
            metrics_service
            .summarize(
                route
            )
        )

        return {

            "profile":
                profile,

            "baseline_distance_km":
                round(
                    baseline_distance_km,
                    3
                ),

            "max_allowed_distance_km":
                round(
                    max_distance_km,
                    3
                ),

            "source_node":
                source_node["node_id"],

            "destination_node":
                destination_node["node_id"],

            "route":
                route,

            "route_length":
                len(route),

            "metrics":
                metrics,

            "risk_metrics": {

                "average_risk":
                    round(
                        avg_risk,
                        4
                    ),

                "max_risk":
                    round(
                        max_risk,
                        4
                    ),

                "risk_node_count":
                    risk_nodes
            }
        }