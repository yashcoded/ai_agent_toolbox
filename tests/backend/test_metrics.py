"""Test metrics API endpoints."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_metrics_overview():
    """Test metrics overview endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/metrics/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_runs" in data
        assert "average_duration_ms" in data
        assert "total_tool_calls" in data


@pytest.mark.asyncio
async def test_agent_stats():
    """Test agent statistics endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/metrics/agent-stats")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
