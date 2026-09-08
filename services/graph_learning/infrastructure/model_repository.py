import mlflow
import mlflow.pytorch

from mlflow.tracking import MlflowClient
from shared.config.ml_config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_MODEL_NAME
)

class ModelRepository:

    EXPERIMENT_NAME = MLFLOW_EXPERIMENT_NAME

    MODEL_NAME = MLFLOW_MODEL_NAME
    SERIALIZATION_FORMAT = (
        "pickle"
    )
    def __init__(self):

        mlflow.set_experiment(
            self.EXPERIMENT_NAME
        )
        mlflow.set_tracking_uri(
            MLFLOW_TRACKING_URI
        )
        self.client = (
            MlflowClient()
        )

        self.active_run = None

    def start_run(
        self,
        run_name: str = None
    ):

        self.active_run = (
            mlflow.start_run(
                run_name=run_name
            )
        )

        return (
            self.active_run
        )

    def end_run(self):

        if mlflow.active_run():

            mlflow.end_run()

    def log_parameter(
        self,
        name: str,
        value
    ):

        mlflow.log_param(
            name,
            value
        )

    def log_metric(
        self,
        name: str,
        value,
        step: int = None
    ):

        mlflow.log_metric(
            key=name,
            value=value,
            step=step
        )

    def save_model(
        self,
        model,
        model_name: str = None,
        parameters: dict = None,
        metrics: dict = None
    ):

        model_name = (
            model_name
            or self.MODEL_NAME
        )

        if parameters:

            for key, value in (
                parameters.items()
            ):

                mlflow.log_param(
                    key,
                    value
                )

        if metrics:

            for key, value in (
                metrics.items()
            ):

                mlflow.log_metric(
                    key,
                    value
                )

        model_info = (
            mlflow.pytorch.log_model(
                pytorch_model=model,
                name="model",
                serialization_format=(
                    self.SERIALIZATION_FORMAT
                )
            )
        )

        try:
            mlflow.register_model(
                model_uri=model_info.model_uri,
                name=model_name
            )

        except Exception as ex:

            print(
                f"Model registration skipped: {ex}"
            )

        return (
            model_info
        )

    def load_model(
        self,
        model_uri: str
    ):

        return (
            mlflow.pytorch.load_model(
                model_uri
            )
        )

    def load_latest_model(
        self,
        model_name: str = None
    ):

        model_name = (
            model_name
            or self.MODEL_NAME
        )

        latest_versions = (
            self.client.get_latest_versions(
                model_name
            )
        )

        if not latest_versions:

            raise ValueError(
                f"No model versions found for "
                f"{model_name}"
            )

        latest_version = (
            latest_versions[0]
        )

        return (
            mlflow.pytorch.load_model(
                latest_version.source
            )
        )

    def get_latest_version(
        self,
        model_name: str = None
    ):

        model_name = (
            model_name
            or self.MODEL_NAME
        )

        latest_versions = (
            self.client.get_latest_versions(
                model_name
            )
        )

        if not latest_versions:

            return None

        return (
            latest_versions[0]
        )