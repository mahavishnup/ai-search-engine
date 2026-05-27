from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Add the 'src' directory to Python path to allow direct imports of core, api, domain, infrastructure, etc.
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from core.config.config import Settings
from core.exceptions.handler import (
    http_exception_handler,
    validation_exception_handler,
    server_exception_handler,
)
from core.logger.logger import setup_logger
from api.v1_router import api_router

# Initialize system configuration and logger
settings = Settings()
logger = setup_logger("backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle operations (startup and shutdown)."""
    logger.info(
        f"Starting {settings.app_name} (API Version: {settings.api_version})..."
    )
    yield
    logger.info(f"Shutting down {settings.app_name}...")


# Create FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug,
    openapi_url=f"/api/{settings.api_version}/openapi.json",
    docs_url=f"/api/{settings.api_version}/docs",
    redoc_url=f"/api/{settings.api_version}/redoc",
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "clientId": "swagger",
        "appName": settings.app_name,
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router, prefix=f"/api/{settings.api_version}")

# Register central exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, server_exception_handler)


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint verifying gateway connectivity."""
    logger.debug("Root endpoint called")
    return {
        "status": "ok",
        "message": f"Welcome to the {settings.app_name} API Gateway",
        "docs": f"/api/{settings.api_version}/docs",
    }


def custom_openapi():
    """Build a custom OpenAPI schema with OAuth2 password flow and Bearer Auth for Swagger UI."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.api_version,
        description="Enterprise-grade AI-Powered Semantic Search Engine API",
        routes=app.routes,
    )

    # Inject security schemes (OAuth2 & Bearer JWT Token)
    openapi_schema.setdefault("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": f"/api/{settings.api_version}/auth/login",
                    "scopes": {},
                }
            },
        },
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Bind custom openapi schema
app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.host, port=settings.port, reload=settings.debug
    )
