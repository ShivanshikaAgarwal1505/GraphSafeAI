import numpy as np
import torch

from torch_geometric.data import Data

from services.graph_learning.feature_registry import (
    FEATURE_COLUMNS
)

from shared.database.models.region import (
    Region
)

from shared.database.models.region_edge import (
    RegionEdge
)

from shared.database.models.safety_feature import (
    SafetyFeature
)

from shared.database.session import (
    SessionLocal
)
 

class DatasetBuilder:

    def build(self):

        db = SessionLocal()

        try:

            regions = (
                db.query(
                    Region
                )
                .order_by(
                    Region.id
                )
                .all()
            )

            region_index = {}

            for idx, region in enumerate(
                regions
            ):

                region_index[
                    region.id
                ] = idx

            features = (
                db.query(
                    SafetyFeature
                )
                .all()
            )

            feature_map = {
                feature.region_id: feature
                for feature in features
            }

            x = []

            y = []

            for region in regions:

                feature = feature_map.get(
                    region.id
                )

                if feature:

                    row = []

                    for column in FEATURE_COLUMNS:

                        row.append(
                            getattr(
                                feature,
                                column,
                                0
                            )
                        )

                    x.append(
                        row
                    )

                    y.append(
                        feature.final_risk
                        if feature.final_risk
                        is not None
                        else 0
                    )

                else:

                    x.append(
                        [
                            0
                            for _
                            in FEATURE_COLUMNS
                        ]
                    )

                    y.append(0)

            edges = (
                db.query(
                    RegionEdge
                )
                .all()
            )

            edge_index = []

            for edge in edges:

                source_id = (
                    edge.source_region_id
                )

                target_id = (
                    edge.target_region_id
                )

                if (
                    source_id
                    not in region_index
                ):
                    continue

                if (
                    target_id
                    not in region_index
                ):
                    continue

                source_idx = (
                    region_index[
                        source_id
                    ]
                )

                target_idx = (
                    region_index[
                        target_id
                    ]
                )

                edge_index.append(
                    [
                        source_idx,
                        target_idx
                    ]
                )

                edge_index.append(
                    [
                        target_idx,
                        source_idx
                    ]
                )

            edge_index = (
                np.array(
                    edge_index
                ).T
            )

            return Data(
                x=torch.tensor(
                    x,
                    dtype=torch.float
                ),

                edge_index=torch.tensor(
                    edge_index,
                    dtype=torch.long
                ),

                y=torch.tensor(
                    y,
                    dtype=torch.float
                )
            )

        finally:

            db.close()