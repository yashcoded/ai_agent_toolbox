"""Tools API endpoints."""

from fastapi import APIRouter
from typing import List, Dict, Any

from app.tools.registry import get_registry

router = APIRouter()


@router.get("/list")
async def list_tools() -> List[Dict[str, Any]]:
    """List all available tools."""
    registry = get_registry()
    return registry.get_tool_metadata()


@router.get("/{tool_name}")
async def get_tool(tool_name: str) -> Dict[str, Any]:
    """Get details about a specific tool."""
    registry = get_registry()
    tools = registry.get_all_tools()
    
    for tool in tools:
        if tool.name == tool_name:
            metadata = registry.get_tool_metadata()
            tool_meta = next((t for t in metadata if t["name"] == tool_name), None)
            return tool_meta or {}
    
    return {"error": "Tool not found"}
