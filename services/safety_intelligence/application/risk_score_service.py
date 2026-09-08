import math

import pandas as pd

from shared.database.models.safety_feature import (
    SafetyFeature
)

from shared.database.models.region import (
    Region
)
import logging

logger = logging.getLogger(__name__)

class RiskScoreService:

    @staticmethod
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

    @staticmethod
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

    def calculate_all(
        self,
        db
    ):

        #
        # Load infrastructure +
        # topology datasets
        #

        topology_df = pd.read_csv(
            "data/processed/topology_features.csv"
        )

        infrastructure_df = pd.read_csv(
            "data/processed/infrastructure_features.csv"
        )

        risk_df = (
            topology_df
            .merge(
                infrastructure_df,
                on="region_id",
                how="left"
            )
        )

        #
        # Normalization
        #

        risk_df[
            "police_distance_norm"
        ] = self.normalize(
            risk_df[
                "nearest_police_distance"
            ]
        )

        risk_df[
            "hospital_distance_norm"
        ] = self.normalize(
            risk_df[
                "nearest_hospital_distance"
            ]
        )

        risk_df[
            "fire_distance_norm"
        ] = self.normalize(
            risk_df[
                "nearest_fire_station_distance"
            ]
        )

        risk_df[
            "dead_end_ratio_norm"
        ] = self.normalize(
            risk_df[
                "dead_end_ratio"
            ]
        )

        risk_df[
            "connectivity_norm"
        ] = self.normalize(
            risk_df[
                "connectivity_score"
            ]
        )

        risk_df[
            "amenity_density_norm"
        ] = self.normalize(
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
        # Safety Features
        #

        features = (
            db.query(
                SafetyFeature
            )
            .all()
        )

        safety_rows = []

        for feature in features:

            safety_rows.append(
                {
                    "region_id":
                        feature.region_id,

                    "report_count":
                        feature.report_count,

                    "avg_severity":
                        feature.avg_severity,

                    "high_severity_count":
                        feature.high_severity_count,

                    "neighbor_report_count":
                        feature.neighbor_report_count,

                    "neighbor_avg_severity":
                        feature.neighbor_avg_severity,
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

            return

        #
        # Normalize incident values
        #

        safety_df[
            "report_count_norm"
        ] = self.normalize(
            safety_df[
                "report_count"
            ]
        )

        safety_df[
            "avg_severity_norm"
        ] = self.normalize(
            safety_df[
                "avg_severity"
            ]
        )

        safety_df[
            "high_severity_norm"
        ] = self.normalize(
            safety_df[
                "high_severity_count"
            ]
        )

        safety_df[
            "neighbor_report_norm"
        ] = self.normalize(
            safety_df[
                "neighbor_report_count"
            ]
        )

        safety_df[
            "neighbor_severity_norm"
        ] = self.normalize(
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

            feature.region_id: feature

            for feature in features
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
                self.incident_confidence(
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
            # Backward compatibility
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

    def calculate_region(
        self,
        db,
        region_id: int
    ):

        feature = (
        db.query(
            SafetyFeature
        )
        .filter(
            SafetyFeature.region_id == region_id
        )
        .first()
        )

        if not feature:
            return

    #
    # Incident risk
    #

        incident_risk = (

        (feature.avg_severity / 5.0) * 0.30

        +

        min(
            feature.report_count / 20.0,
            1.0
        ) * 0.25

        +

        min(
            feature.high_severity_count / 10.0,
            1.0
        ) * 0.15

        +

        min(
            feature.neighbor_report_count / 20.0,
            1.0
        ) * 0.15

        +

        min(
            feature.neighbor_avg_severity / 5.0,
            1.0
        ) * 0.10

        +

        min(
            feature.incident_growth_rate,
            1.0
        ) * 0.05
        )

        feature.incident_risk = (
            incident_risk
        )

        confidence = self.incident_confidence(
        feature.report_count
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

        feature.structural_risk
        * structural_weight

        +

        incident_risk
        * incident_weight
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

        feature.safety_score = (
        final_risk
        )

        
        logger.info(
        "[FEATURES] region=%s reports=%s severity=%.2f neighbors=%s",
            region_id,incident_risk,final_risk
        )

        db.flush()