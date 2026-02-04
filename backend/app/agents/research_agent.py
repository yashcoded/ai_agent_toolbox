"""Research Agent - for information gathering and analysis."""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from typing import List, Dict, Any
import asyncio

from app.core.config import settings
from app.tools.registry import get_tools_for_agent


class ResearchAgent:
    """Research agent for gathering and analyzing information."""
    
    def __init__(self):
        """Initialize research agent."""
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_MODEL,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
            streaming=True,
        )
        self.tools = get_tools_for_agent("research")
        self.agent = self._create_agent()
        
    def _create_agent(self):
        """Create the agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research assistant AI agent. Your job is to:
1. Gather information from various sources
2. Analyze and synthesize information
3. Provide well-structured, accurate responses
4. Use available tools effectively

Be thorough, accurate, and cite your sources when possible."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=settings.MAX_ITERATIONS,
        )
    
    async def run(self, query: str) -> Dict[str, Any]:
        """Run the research agent."""
        result = await self.agent.ainvoke({"input": query})
        return result
    
    async def stream(self, query: str):
        """Stream the research agent responses."""
        async for chunk in self.agent.astream({"input": query}):
            yield chunk
