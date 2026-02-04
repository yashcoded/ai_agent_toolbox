"""Code Agent - for code analysis and generation."""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, Any

from app.core.config import settings
from app.tools.registry import get_tools_for_agent


class CodeAgent:
    """Code agent for analyzing and generating code."""
    
    def __init__(self):
        """Initialize code agent."""
        self.llm = ChatOpenAI(
            model=settings.DEFAULT_MODEL,
            temperature=0.2,  # Lower temperature for code generation
            api_key=settings.OPENAI_API_KEY,
            streaming=True,
        )
        self.tools = get_tools_for_agent("code")
        self.agent = self._create_agent()
        
    def _create_agent(self):
        """Create the agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a coding assistant AI agent. Your job is to:
1. Analyze code and identify issues
2. Generate clean, well-documented code
3. Suggest improvements and best practices
4. Debug and fix code problems
5. Use available tools effectively

Write clean, efficient code following best practices."""),
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
        """Run the code agent."""
        result = await self.agent.ainvoke({"input": query})
        return result
    
    async def stream(self, query: str):
        """Stream the code agent responses."""
        async for chunk in self.agent.astream({"input": query}):
            yield chunk
