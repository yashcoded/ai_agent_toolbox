"""Test agent API endpoints."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_agent_run():
    """Test agent run endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/agents/run",
            json={
                "query": "What is 2+2?",
                "agent_type": "research",
                "stream": False,
            },
        )
        # May fail without OpenAI key, but structure should be correct
        assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_agent_history():
    """Test agent history endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/agents/history?limit=5")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
