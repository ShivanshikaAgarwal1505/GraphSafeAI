import torch
import mlflow

from services.graph_learning.infrastructure.dataset_builder import (
    DatasetBuilder
)

from services.graph_learning.infrastructure.model_repository import (
    ModelRepository
)

from services.graph_learning.models.graphsage_model import (
    GraphSAGEModel
)

from services.graph_learning.infrastructure.evaluator import (
    Evaluator
)

from shared.config.ml_config import (
    GRAPHSAGE_EPOCHS,
    GRAPHSAGE_HIDDEN_CHANNELS,
    GRAPHSAGE_LEARNING_RATE,
    MLFLOW_MODEL_NAME
)

class Trainer:

    DEFAULT_EPOCHS = GRAPHSAGE_EPOCHS

    DEFAULT_HIDDEN_CHANNELS = GRAPHSAGE_HIDDEN_CHANNELS

    DEFAULT_LEARNING_RATE = GRAPHSAGE_LEARNING_RATE

    def __init__(self):

        self.dataset_builder = (
            DatasetBuilder()
        )

        self.model_repository = (
            ModelRepository()
        )
        self.evaluator = (
            Evaluator()
        )

    def train(
        self,
        epochs: int = DEFAULT_EPOCHS,
        hidden_channels: int = DEFAULT_HIDDEN_CHANNELS,
        learning_rate: float = DEFAULT_LEARNING_RATE
    ):

        self.model_repository.start_run(
            run_name="graphsage_training"
        )

        try:

            data = (
                self.dataset_builder
                .build()
            )

            model = GraphSAGEModel(
                in_channels=data.num_features,
                hidden_channels=hidden_channels
            )

            optimizer = (
                torch.optim.Adam(
                    model.parameters(),
                    lr=learning_rate
                )
            )

            criterion = (
                torch.nn.MSELoss()
            )

            final_loss = None

            for epoch in range(
                epochs
            ):

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

                final_loss = (
                    loss.item()
                )

                self.model_repository.log_metric(
                    name="loss",
                    value=final_loss,
                    step=epoch
                )

                if epoch % 20 == 0:

                    print(
                        f"Epoch {epoch}: "
                        f"{final_loss:.6f}"
                    )
            
            model.eval()
            with torch.no_grad():

                predictions = model(
                    data.x,
                    data.edge_index
                )

                predictions = (
                    predictions
                    .cpu()
                    .numpy()
                )

            targets = (
                data.y
                .cpu()
                .numpy()
            )

            metrics = (
                self.evaluator
                .evaluate(
                    targets,
                    predictions
                )
            )
            mlflow.log_metric(
                "final_loss",
                loss.item()
            )
            mlflow.log_metric(
                "rmse",
                metrics["rmse"]
            )

            mlflow.log_metric(
                "mae",
                metrics["mae"]
            )

            mlflow.log_metric(
                "r2",
                metrics["r2"]
            )
            
            self.model_repository.save_model(
                model=model,
                model_name=MLFLOW_MODEL_NAME,
                parameters={
                    "epochs": epochs,
                    "hidden_channels": hidden_channels,
                    "learning_rate": learning_rate
                },
                metrics={
                    "final_loss": final_loss,
                    "rmse": metrics["rmse"],
                    "mae": metrics["mae"],
                    "r2": metrics["r2"]
                }
            )

            return model

        finally:

            self.model_repository.end_run()