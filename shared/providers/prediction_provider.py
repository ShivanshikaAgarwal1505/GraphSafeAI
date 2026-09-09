from shared.database.models.prediction import (
    Prediction
)


class PredictionProvider:

    def get_prediction_map(
        self,
        db
    ):

        rows = (
            db.query(
                Prediction
            )
            .all()
        )

        return {

            row.region_id:
            row.prediction_score

            for row in rows
        }