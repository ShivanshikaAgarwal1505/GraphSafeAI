from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import numpy as np


class Evaluator:

    def evaluate(
        self,
        y_true,
        y_pred
    ):

        y_true = np.asarray(
            y_true
        )

        y_pred = np.asarray(
            y_pred
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_true,
                y_pred
            )
        )

        mae = mean_absolute_error(
            y_true,
            y_pred
        )

        r2 = r2_score(
            y_true,
            y_pred
        )

        return {
            "rmse": float(rmse),
            "mae": float(mae),
            "r2": float(r2)
        }
