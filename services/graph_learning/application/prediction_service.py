from datetime import datetime

from services.graph_learning.infrastructure.predictor import (
    Predictor
)

from shared.database.models.prediction import (
    Prediction
)

from shared.database.models.region import (
    Region
)

class PredictionService:

    def __init__(self):

        self.predictor = (
            Predictor()
        )

    def generate_predictions(
    self,
    db
    ):

        predictions = (
        self.predictor
        .predict_all()
        )

        model_version = (
        self.predictor
        .get_model_version()
        )

        regions = (
        db.query(
            Region
        )
        .order_by(
            Region.id
        )
        .all()
        )

        db.query(
        Prediction
        ).delete()

        db.flush()

        records_created = 0

        for region, prediction in zip(
        regions,
        predictions
        ):

            db.add(
            Prediction(
                region_id=region.id,
                prediction_score=float(
                    prediction
                ),
                model_version=model_version,
                generated_at=datetime.utcnow()
            )
            )

            records_created += 1

        db.commit()

        return {
        "regions_processed": records_created,
        "model_version": model_version
        }
    
    def get_prediction(
        self,
        db,
        region_id: int
    ):

        return (
            db.query(
                Prediction
            )
            .filter(
                Prediction.region_id
                == region_id
            )
            .first()
        )

    def get_predictions(
        self,
        db
    ):

        return (
            db.query(
                Prediction
            )
            .all()
        )