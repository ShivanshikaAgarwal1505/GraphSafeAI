from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from shared.database.session import get_db

from services.graph_learning.infrastructure.trainer import (
    Trainer
)

from services.graph_learning.application.prediction_service import (
    PredictionService
)

router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Graph Learning"]
)


@router.post("/train")
def train_model():

    Trainer().train()

    return {
        "status": "completed"
    }


@router.post("/predictions/generate")
def generate_predictions(
    db=Depends(get_db)
):

    return (
        PredictionService()
        .generate_predictions(db)
    )


@router.get("/predictions")
def get_predictions(
    db=Depends(get_db)
):

    return (
        PredictionService()
        .get_predictions(db)
    )


@router.get("/predictions/{region_id}")
def get_prediction(
    region_id: int,
    db=Depends(get_db)
):

    prediction = (
        PredictionService()
        .get_prediction(
            db,
            region_id
        )
    )

    if prediction is None:

        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return prediction