from pathlib import Path

import pandas as pd
import torch

from torch_geometric.data import Data

from services.graph_learning.feature_registry import (
    FEATURE_COLUMNS
)

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