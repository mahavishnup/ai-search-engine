"""Pytest configuration and shared fixtures."""

from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for API testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
