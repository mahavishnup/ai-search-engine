from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from ..logger.logger import setup_logger

logger = setup_logger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning("HTTP error: %s %s", request.url, exc.detail)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error: %s %s", request.url, exc.errors())
    return JSONResponse({"detail": exc.errors()}, status_code=422)


async def server_exception_handler(request: Request, exc: Exception):
    logger.error("Unexpected server error: %s", exc, exc_info=True)
    return JSONResponse({"detail": "Internal Server Error"}, status_code=500)
