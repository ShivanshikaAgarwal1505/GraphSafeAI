from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.config.settings import settings

from services.community_reporting.api.v1.routes import (
    router as report_router
)

from services.graph_learning.api.routes import (
    router as graph_learning_router
)

from services.routing_engine.api.routes import (
    router as routing_router
)

from services.navigation_engine.api.routes import (
    router as navigation_router
)

from services.authentication.api.routes import (
    router as auth_router,
)

from services.favorites.api.routes import (
    router as favorites_router,
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

# ----------------------------
# CORS
# ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:19006",
        "http://127.0.0.1:19006",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Routes
# ----------------------------

app.include_router(
    report_router,
    prefix="/api/v1/reports",
    tags=["Reports"]
)

app.include_router(
    graph_learning_router
)

app.include_router(
    routing_router
)

app.include_router(
    navigation_router
)

app.include_router(
    auth_router,
)

app.include_router(
    favorites_router,
)
# ----------------------------
# Health
# ----------------------------

@app.get("/")
async def root():
    return {
        "message": "GraphSafeAI API Running"
    } 