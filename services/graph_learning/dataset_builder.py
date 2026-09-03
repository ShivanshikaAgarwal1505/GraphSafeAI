from pathlib import Path

import pandas as pd
import torch

from torch_geometric.data import Data


FEATURE_COLUMNS = [

    # Safety

    "report_count",
    "avg_severity",
    "neighbor_report_count",
    "neighbor_avg_severity",
    "degree",

    # Topology

    "node_count",
    "avg_degree",

    "dead_end_count",
    "intersection_count",

    "dead_end_ratio",
    "intersection_density",

    "connectivity_score",

    # Infrastructure

    "police_count",
    "hospital_count",
    "school_count",
    "fire_station_count",

    "amenity_count",
    "amenity_density",
]

class DatasetBuilder:

    def build(self):

        data_dir = Path(
            "data/processed"
        )

        node_df = pd.read_csv(
            data_dir / "node_features.csv"
        )

        edge_df = pd.read_csv(
            data_dir / "edge_list.csv"
        )

        x = torch.tensor(
            node_df[
                FEATURE_COLUMNS
            ].values,
            dtype=torch.float,
        )

        y = torch.tensor(
            node_df[
                "safety_score"
            ].values,
            dtype=torch.float,
        )

        edge_index = torch.tensor(
            edge_df[
                [
                    "source_region_id",
                    "target_region_id",
                ]
            ].values.T,
            dtype=torch.long,
        )

        edge_index = edge_index - 1

        return Data(
            x=x,
            edge_index=edge_index,
            y=y,
        )