"""Tests for the health check and root endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Test that the /api/health endpoint returns 200 OK and correct JSON response."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    """Test that the root endpoint (/) returns correct API gateway welcome message."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Welcome to the" in data["message"]
    assert "docs" in data
