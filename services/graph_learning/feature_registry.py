from shared.geo.osm.amenity_config import (
    AMENITY_TYPES
)

SAFETY_FEATURES = [

    "report_count",
    "avg_severity",

    "high_severity_count",
    "recent_report_count",

    "incident_diversity",

    "reports_last_7_days",
    "reports_last_30_days",
    "reports_last_90_days",

    "incident_growth_rate",

    "theft_count",
    "harassment_count",
    "accident_count",
    "unsafe_area_count",
    "streetlight_failure_count",

    "neighbor_report_count",
    "neighbor_avg_severity",
    "neighbor_incident_diversity",

    "degree",

    "structural_risk",
    "incident_risk",
    "incident_confidence",
    "structural_weight",
    "incident_weight",
    "final_risk",
]

TOPOLOGY_FEATURES = [
    "node_count",
    "avg_degree",

    "dead_end_count",
    "intersection_count",

    "dead_end_ratio",
    "intersection_density",

    "connectivity_score",
]

INFRASTRUCTURE_FEATURES = []

for amenity in AMENITY_TYPES:

    INFRASTRUCTURE_FEATURES.append(
        f"{amenity}_count"
    )

INFRASTRUCTURE_FEATURES.append(
    "amenity_count"
)

INFRASTRUCTURE_FEATURES.append(
    "amenity_density"
)

for amenity in AMENITY_TYPES:

    INFRASTRUCTURE_FEATURES.append(
        f"{amenity}_density"
    )

DISTANCE_FEATURES = []

for amenity in AMENITY_TYPES:

    DISTANCE_FEATURES.append(
        f"nearest_{amenity}_distance"
    )

FEATURE_COLUMNS = (
    SAFETY_FEATURES
    + TOPOLOGY_FEATURES
    + INFRASTRUCTURE_FEATURES
    + DISTANCE_FEATURES
)