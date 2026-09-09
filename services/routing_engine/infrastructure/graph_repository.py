from collections import defaultdict

from shared.database.models.region_edge import (
    RegionEdge
)

from shared.database.models.safety_feature import (
    SafetyFeature
)

from shared.database.models.prediction import (
    Prediction
)

class GraphRepository:

    def build_graph(
        self,
        db
    ):

        adjacency = defaultdict(list)

        edges = (
            db.query(
                RegionEdge
            )
            .all()
        )

        for edge in edges:

            adjacency[
                edge.source_region_id
            ].append(
                edge.target_region_id
            )

            adjacency[
                edge.target_region_id
            ].append(
                edge.source_region_id
            )

        return adjacency

    def risk_map(
        self,
        db
    ):

        rows = (
            db.query(
                SafetyFeature
            )
            .all()
        )

        return {
            row.region_id:
            float(
                row.final_risk or 0
            )
            for row in rows
        }
        
    def prediction_map(
    self,
    db
    ):

        rows = (
        db.query(
            Prediction
        )
        .all()
        )

        return {
        row.region_id:
        float(
            row.prediction_score
        )
        for row in rows
        }