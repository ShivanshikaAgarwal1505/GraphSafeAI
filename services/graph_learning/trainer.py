import torch

from services.graph_learning.dataset_builder import (
    DatasetBuilder
)

from services.graph_learning.graphsage_model import (
    GraphSAGEModel
)


class Trainer:

    def train(self):

        data = (
            DatasetBuilder()
            .build()
        )

        model = (
            GraphSAGEModel()
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

        for epoch in range(200):

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