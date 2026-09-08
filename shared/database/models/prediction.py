from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from shared.database.models.base import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True
    )

    region_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    prediction_score = Column(
        Float,
        nullable=False
    )

    model_version = Column(
        String,
        nullable=False
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow
    )