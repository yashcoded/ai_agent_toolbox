"""
Tests for tool functionality
"""
import pytest
from backend.tools import calculator, code_exec, get_available_tools


def test_calculator():
    """Test calculator tool"""
    # Test simple calculation
    result = calculator("2 + 2")
    assert result == "4"
    
    # Test multiplication
    result = calculator("10 * 5")
    assert result == "50"
    
    # Test complex expression
    result = calculator("(10 + 5) * 2")
    assert result == "30"


def test_code_exec_simple():
    """Test code execution with simple Python code"""
    code = "print('Hello, World!')"
    result = code_exec(code, "python")
    assert "Hello, World!" in result


def test_code_exec_calculation():
    """Test code execution with calculation"""
    code = """
result = 10 + 20
print(result)
"""
    result = code_exec(code, "python")
    assert "30" in result


def test_code_exec_error():
    """Test code execution with error"""
    code = "print(undefined_variable)"
    result = code_exec(code, "python")
    assert "Error" in result or "NameError" in result


def test_get_available_tools():
    """Test getting available tools"""
    tools = get_available_tools()
    assert len(tools) == 3
    
    tool_names = [tool.name for tool in tools]
    assert "web_search" in tool_names
    assert "calculator" in tool_names
    assert "code_exec" in tool_names
