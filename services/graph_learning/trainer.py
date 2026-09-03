import torch

from services.graph_learning.dataset_builder import (
    DatasetBuilder
)

from services.graph_learning.graphsage_model import (
    GraphSAGEModel
)
EPOCH=250
class Trainer:

    def train(self):

        data = (
            DatasetBuilder()
            .build()
        )

        model = (
            GraphSAGEModel(data.num_features, hidden_channels=32)
        )

        optimizer = (
            torch.optim.Adam(
                model.parameters(),
                lr=0.01
            )
        )

        criterion = (
            torch.nn.MSELoss()
        )

        for epoch in range(EPOCH):

            model.train()

            optimizer.zero_grad()

            prediction = model(
                data.x,
                data.edge_index
            )

            loss = criterion(
                prediction,
                data.y
            )

            loss.backward()

            optimizer.step()

            if epoch % 20 == 0:

                print(
                    f"Epoch {epoch}: "
                    f"{loss.item():.4f}"
                )

        return model