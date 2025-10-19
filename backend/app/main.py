from __future__ import annotations

import logging
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routers import scripts as scripts_router
from .routers import storyboards as storyboards_router
from .routers import camera as camera_router


logger = logging.getLogger("uvicorn.error")


def create_app() -> FastAPI:
    app = FastAPI(title="Script & Storyboard API", version="0.1.0")

    # CORS
    origins: List[str] = settings.cors_origins or ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(scripts_router.router)
    app.include_router(storyboards_router.router)
    app.include_router(camera_router.router)

    @app.on_event("startup")
    def on_startup():
        logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
        logger.info("Application started. Environment=%s", settings.environment)

    @app.exception_handler(Exception)
    async def handle_exceptions(request: Request, exc: Exception):
        logger.exception("Unhandled error: %s", exc)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    return app


app = create_app()
