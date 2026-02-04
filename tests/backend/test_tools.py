"""Test tools API endpoints."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_list_tools():
    """Test listing all tools."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/tools/list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check structure
        assert "name" in data[0]
        assert "description" in data[0]
        assert "agent_types" in data[0]


@pytest.mark.asyncio
async def test_get_tool():
    """Test getting a specific tool."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/tools/calculator")
        assert response.status_code == 200
        data = response.json()
        assert data.get("name") == "calculator"
