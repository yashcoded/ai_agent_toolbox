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
    assert "production" in prompt.lower()
    assert "agent" in prompt.lower()


@pytest.mark.asyncio
async def test_create_agent_requires_api_key():
    """Test agent creation requires API key"""
    # Without API key, agent creation should fail
    import os
    if not os.getenv("OPENAI_API_KEY"):
        with pytest.raises(Exception):
            agent = create_agent()


@pytest.mark.asyncio
async def test_agent_structure():
    """Test agent structure if API key is available"""
    import os
    if os.getenv("OPENAI_API_KEY"):
        agent = create_agent()
        assert agent is not None
        assert agent.tools is not None
        assert len(agent.tools) > 0
    else:
        pytest.skip("Skipping test - OPENAI_API_KEY not set")
