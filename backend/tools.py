"""
Tool implementations for the AI agent
"""
from langchain.tools import Tool
from typing import List
import os
import re
import subprocess
import tempfile


def web_search(query: str) -> str:
    """
    Search the web for information
    """
    try:
        # Use SerpAPI if available
        api_key = os.getenv("SERPER_API_KEY") or os.getenv("SERPAPI_API_KEY")
        if api_key:
            from langchain_community.utilities import SerpAPIWrapper
            search = SerpAPIWrapper(serpapi_api_key=api_key)
            return search.run(query)
        else:
            # Fallback: return a placeholder
            return f"Web search for '{query}': Feature requires SERPER_API_KEY or SERPAPI_API_KEY environment variable."
    except Exception as e:
        return f"Error performing web search: {str(e)}"


def calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions
    """
    try:
        # Remove any non-mathematical characters for safety
        expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


def code_exec(code: str, language: str = "python") -> str:
    """
    Execute code in a sandboxed environment
    """
    try:
        if language.lower() == "python":
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute with timeout
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return result.stdout or "Code executed successfully (no output)"
            else:
                return f"Error: {result.stderr}"
        else:
            return f"Language '{language}' not supported. Only Python is currently supported."
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (5 second limit)"
    except Exception as e:
        return f"Error executing code: {str(e)}"


def get_available_tools() -> List[Tool]:
    """
    Get list of all available tools for the agent
    """
    tools = [
        Tool(
            name="web_search",
            func=web_search,
            description="Search the web for current information. Input should be a search query string. Use this when you need up-to-date information or facts from the internet."
        ),
        Tool(
            name="calculator",
            func=calculator,
            description="Perform mathematical calculations. Input should be a mathematical expression like '2 + 2' or '10 * 5 + 3'. Use this for any arithmetic operations."
        ),
        Tool(
            name="code_exec",
            func=lambda code: code_exec(code, "python"),
            description="Execute Python code in a sandboxed environment. Input should be valid Python code. Use this to run computations, data processing, or testing code snippets. Timeout is 5 seconds."
        ),
    ]
    
    return tools
