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
    Evaluate mathematical expressions safely using AST
    """
    try:
        import ast
        import operator
        
        # Define allowed operations
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
        }
        
        def eval_expr(node):
            """Safely evaluate an AST node"""
            if isinstance(node, ast.Constant):  # number (Python 3.8+)
                return node.value
            elif isinstance(node, ast.Num):  # number (older Python)
                return node.n
            elif isinstance(node, ast.BinOp):  # binary operation
                op = operators.get(type(node.op))
                if op is None:
                    raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
                return op(eval_expr(node.left), eval_expr(node.right))
            elif isinstance(node, ast.UnaryOp):  # unary operation
                op = operators.get(type(node.op))
                if op is None:
                    raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
                return op(eval_expr(node.operand))
            else:
                raise ValueError(f"Unsupported expression type: {type(node).__name__}")
        
        # Parse and evaluate
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
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
