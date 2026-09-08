import torch

from services.graph_learning.infrastructure.dataset_builder import (
    DatasetBuilder
)

from services.graph_learning.infrastructure.model_repository import (
    ModelRepository
)


class Predictor:

    def __init__(self):

        self.dataset_builder = (
            DatasetBuilder()
        )

        self.model_repository = (
            ModelRepository()
        )

    def predict_all(self):

        data = (
            self.dataset_builder
            .build()
        )

        model = (
            self.model_repository
            .load_latest_model()
        )

        model.eval()

        with torch.no_grad():

            predictions = model(
                data.x,
                data.edge_index
            )

        return (
            predictions
            .cpu()
            .numpy()
        )

    def get_model_version(self):

        latest_version = (
            self.model_repository
            .get_latest_version()
        )

        if latest_version is None:

            return "unknown"

        return str(
            latest_version.version
        )