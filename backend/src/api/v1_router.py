"""API v1 router aggregating all endpoints."""

from fastapi import APIRouter
from api.routes.health import router as health_router

api_router = APIRouter()

# Include all route modules under unified API v1 router
api_router.include_router(health_router)
