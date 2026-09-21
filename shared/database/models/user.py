from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)

from shared.database.models.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    reputation_score = Column(
        Integer,
        default=0,
    )

    reports_submitted = Column(
        Integer,
        default=0,
    )

    reports_verified = Column(
        Integer,
        default=0,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
    
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )
    
    last_login_at = Column(
        DateTime,
        nullable=True,
    )