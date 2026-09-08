from fastapi import FastAPI

from shared.config.settings import settings

from services.community_reporting.api.v1.routes import (
    router as report_router
)

from services.graph_learning.api.routes import (
    router as graph_learning_router
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(name)s "
        "%(message)s"
    )
)
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(
    report_router,
    prefix="/api/v1/reports",
    tags=["Reports"]
)


@app.get("/")
async def root():
    return {
        "message": "GraphSafeAI API Running"
    }
    

app.include_router(
    graph_learning_router
)