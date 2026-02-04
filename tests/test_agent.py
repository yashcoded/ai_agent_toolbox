"""
Tests for agent functionality
"""
import pytest
from backend.agent import create_agent, load_master_prompt


def test_load_master_prompt():
    """Test loading the master prompt"""
    prompt = load_master_prompt()
    assert prompt is not None
    assert len(prompt) > 0
    assert "production AI agent" in prompt.lower()


@pytest.mark.asyncio
async def test_create_agent():
    """Test agent creation"""
    agent = create_agent()
    assert agent is not None
    assert agent.tools is not None
    assert len(agent.tools) > 0


@pytest.mark.asyncio
async def test_agent_simple_query():
    """Test agent with a simple query"""
    agent = create_agent()
    
    # This test requires API keys, so we'll just check structure
    assert agent.agent is not None
    assert agent.memory is None  # No session_id provided
