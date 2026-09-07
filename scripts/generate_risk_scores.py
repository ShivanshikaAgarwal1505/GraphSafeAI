import math

import pandas as pd

from shared.database.session import SessionLocal

from shared.database.models.region import (
    Region
)
from shared.database.models.region import (
    Region
)

from shared.database.models.region_edge import (
    RegionEdge
)

from shared.database.models.community_report import (
    CommunityReport
)

from shared.database.models.safety_feature import (
    SafetyFeature
)

def normalize(series):

    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(
            0,
            index=series.index
        )

    return (
        series - min_value
    ) / (
        max_value - min_value
    )


def incident_confidence(
    report_count
):

    return (
        1
        -
        math.exp(
            -report_count / 10
        )
    )


def main():

    db = SessionLocal()

    #
    # Load generated datasets
    #

    topology_df = pd.read_csv(
        "data/processed/topology_features.csv"
    )

    infrastructure_df = pd.read_csv(
        "data/processed/infrastructure_features.csv"
    )

    #
    # Merge feature datasets
    #

    risk_df = (
        topology_df
        .merge(
            infrastructure_df,
            on="region_id",
            how="left"
        )
    )

    #
    # Normalize structural fields
    #

    risk_df[
        "police_distance_norm"
    ] = normalize(
        risk_df[
            "nearest_police_distance"
        ]
    )

    risk_df[
        "hospital_distance_norm"
    ] = normalize(
        risk_df[
            "nearest_hospital_distance"
        ]
    )

    risk_df[
        "fire_distance_norm"
    ] = normalize(
        risk_df[
            "nearest_fire_station_distance"
        ]
    )

    risk_df[
        "dead_end_ratio_norm"
    ] = normalize(
        risk_df[
            "dead_end_ratio"
        ]
    )

    risk_df[
        "connectivity_norm"
    ] = normalize(
        risk_df[
            "connectivity_score"
        ]
    )

    risk_df[
        "amenity_density_norm"
    ] = normalize(
        risk_df[
            "amenity_density"
        ]
    )

    #
    # Structural Risk
    #

    risk_df[
        "structural_risk"
    ] = (

        risk_df[
            "police_distance_norm"
        ] * 0.20

        +

        risk_df[
            "hospital_distance_norm"
        ] * 0.20

        +

        risk_df[
            "fire_distance_norm"
        ] * 0.15

        +

        risk_df[
            "dead_end_ratio_norm"
        ] * 0.15

        +

        (
            1
            -
            risk_df[
                "connectivity_norm"
            ]
        ) * 0.15

        +

        (
            1
            -
            risk_df[
                "amenity_density_norm"
            ]
        ) * 0.15

    )

    #
    # Load Safety Features
    #

    features = (
        db.query(
            SafetyFeature
        )
        .all()
    )

    #
    # Create dataframe
    #

    safety_rows = []

    for f in features:

        safety_rows.append(
            {
                "region_id":
                    f.region_id,

                "report_count":
                    f.report_count,

                "avg_severity":
                    f.avg_severity,

                "high_severity_count":
                    f.high_severity_count,

                "neighbor_report_count":
                    f.neighbor_report_count,

                "neighbor_avg_severity":
                    f.neighbor_avg_severity,
            }
        )

    safety_df = pd.DataFrame(
        safety_rows
    )

    if len(
        safety_df
    ) == 0:

        print(
            "No safety features found."
        )

        db.close()
        return

    #
    # Normalize incident data
    #

    safety_df[
        "report_count_norm"
    ] = normalize(
        safety_df[
            "report_count"
        ]
    )

    safety_df[
        "avg_severity_norm"
    ] = normalize(
        safety_df[
            "avg_severity"
        ]
    )

    safety_df[
        "high_severity_norm"
    ] = normalize(
        safety_df[
            "high_severity_count"
        ]
    )

    safety_df[
        "neighbor_report_norm"
    ] = normalize(
        safety_df[
            "neighbor_report_count"
        ]
    )

    safety_df[
        "neighbor_severity_norm"
    ] = normalize(
        safety_df[
            "neighbor_avg_severity"
        ]
    )

    #
    # Incident Risk
    #

    safety_df[
        "incident_risk"
    ] = (

        safety_df[
            "report_count_norm"
        ] * 0.25

        +

        safety_df[
            "avg_severity_norm"
        ] * 0.25

        +

        safety_df[
            "high_severity_norm"
        ] * 0.20

        +

        safety_df[
            "neighbor_report_norm"
        ] * 0.15

        +

        safety_df[
            "neighbor_severity_norm"
        ] * 0.15

    )

    #
    # Combine
    #

    merged = (
        safety_df[
            [
                "region_id",
                "incident_risk",
                "report_count"
            ]
        ]
        .merge(
            risk_df[
                [
                    "region_id",
                    "structural_risk"
                ]
            ],
            on="region_id",
            how="left"
        )
    )

    #
    # Persist
    #

    features_by_region = {
        f.region_id: f
        for f in features
    }

    for _, row in merged.iterrows():

        region_id = row[
            "region_id"
        ]

        feature = (
            features_by_region[
                region_id
            ]
        )

        structural_risk = float(
            row[
                "structural_risk"
            ]
        )

        incident_risk = float(
            row[
                "incident_risk"
            ]
        )

        confidence = (
            incident_confidence(
                row[
                    "report_count"
                ]
            )
        )

        structural_confidence = 1.0

        total = (
            structural_confidence
            +
            confidence
        )

        structural_weight = (
            structural_confidence
            / total
        )

        incident_weight = (
            confidence
            / total
        )

        final_risk = (

            structural_risk
            *
            structural_weight

            +

            incident_risk
            *
            incident_weight

        )

        feature.structural_risk = (
            structural_risk
        )

        feature.incident_risk = (
            incident_risk
        )

        feature.incident_confidence = (
            confidence
        )

        feature.structural_weight = (
            structural_weight
        )

        feature.incident_weight = (
            incident_weight
        )

        feature.final_risk = (
            final_risk
        )

        #
        # keep backward compatibility
        #

        feature.safety_score = (
            final_risk
        )

    db.commit()

    print()
    print(
        "Risk scores generated."
    )
    print(
        f"Regions: {len(features)}"
    )

    db.close()


if __name__ == "__main__":
    main()