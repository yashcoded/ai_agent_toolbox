"""Tool registry for managing agent tools."""

from typing import List, Dict, Any
from langchain_core.tools import Tool
from functools import lru_cache


class ToolRegistry:
    """Registry for managing tools available to agents."""
    
    def __init__(self):
        """Initialize tool registry."""
        self._tools: Dict[str, Tool] = {}
        self._agent_tools: Dict[str, List[str]] = {
            "research": [],
            "code": [],
            "general": [],
        }
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools."""
        # Calculator tool
        calculator_tool = Tool(
            name="calculator",
            description="Useful for performing mathematical calculations. Input should be a mathematical expression.",
            func=self._calculate,
        )
        self.register_tool(calculator_tool, ["research", "code", "general"])
        
        # Search tool (mock)
        search_tool = Tool(
            name="search",
            description="Search for information on the web. Input should be a search query.",
            func=self._search,
        )
        self.register_tool(search_tool, ["research", "general"])
        
        # Code analyzer tool
        code_analyzer_tool = Tool(
            name="code_analyzer",
            description="Analyze code for potential issues and improvements. Input should be code snippet.",
            func=self._analyze_code,
        )
        self.register_tool(code_analyzer_tool, ["code", "general"])
    
    def register_tool(self, tool: Tool, agent_types: List[str]):
        """Register a tool for specific agent types."""
        self._tools[tool.name] = tool
        for agent_type in agent_types:
            if agent_type in self._agent_tools:
                if tool.name not in self._agent_tools[agent_type]:
                    self._agent_tools[agent_type].append(tool.name)
    
    def get_tools_for_agent(self, agent_type: str) -> List[Tool]:
        """Get all tools available for a specific agent type."""
        tool_names = self._agent_tools.get(agent_type, [])
        return [self._tools[name] for name in tool_names if name in self._tools]
    
    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_tool_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all tools."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "agent_types": [
                    agent_type
                    for agent_type, tools in self._agent_tools.items()
                    if tool.name in tools
                ],
            }
            for tool in self._tools.values()
        ]
    
    @staticmethod
    def _calculate(expression: str) -> str:
        """Calculate mathematical expression."""
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    @staticmethod
    def _search(query: str) -> str:
        """Mock search function."""
        return f"Search results for '{query}': [Mock results - integrate real search API]"
    
    @staticmethod
    def _analyze_code(code: str) -> str:
        """Analyze code snippet."""
        lines = code.split('\n')
        analysis = f"Code Analysis:\n"
        analysis += f"- Lines of code: {len(lines)}\n"
        analysis += f"- Characters: {len(code)}\n"
        
        # Simple checks
        if 'TODO' in code:
            analysis += "- Contains TODO items\n"
        if 'FIXME' in code:
            analysis += "- Contains FIXME items\n"
        
        return analysis


# Global registry instance
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Get the global tool registry."""
    return _registry


def get_tools_for_agent(agent_type: str) -> List[Tool]:
    """Get tools for a specific agent type."""
    return _registry.get_tools_for_agent(agent_type)
