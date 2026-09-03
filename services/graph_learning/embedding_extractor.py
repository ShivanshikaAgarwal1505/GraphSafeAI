import torch

from services.graph_learning.dataset_builder import (
    DatasetBuilder
)

from services.graph_learning.graphsage_model import (
    GraphSAGEModel
)


class EmbeddingExtractor:

    def extract(self):

        data = (
            DatasetBuilder()
            .build()
        )

        model = GraphSAGEModel(data.num_features, hidden_channels=32)

        model.load_state_dict(
            torch.load(
                "models/graphsage/model.pt"
            )
        )

        model.eval()

        with torch.no_grad():

            embeddings = model.conv1(
                data.x,
                data.edge_index
            )

            embeddings = torch.relu(
                embeddings
            )

            embeddings = model.conv2(
                embeddings,
                data.edge_index
            )

            embeddings = torch.relu(
                embeddings
            )

        return embeddings