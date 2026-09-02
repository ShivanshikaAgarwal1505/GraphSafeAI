from sqlalchemy import create_engine

from shared.config.settings import settings


engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG
)