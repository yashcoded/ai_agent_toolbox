"""
FastAPI main application for AI Agent Toolbox
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import logging

# Try relative imports first, then absolute
try:
    from .agent import create_agent, AgentCallbackHandler
    from .tools import get_available_tools
    from .db import get_db_connection, log_interaction, get_evals
    from .evals import EvalResult
except ImportError:
    from agent import create_agent, AgentCallbackHandler
    from tools import get_available_tools
    from db import get_db_connection, log_interaction, get_evals
    from evals import EvalResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Agent Toolbox", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ToolRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "AI Agent Toolbox"}


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint using Server-Sent Events (SSE)
    """
    async def event_generator():
        try:
            agent = create_agent(session_id=request.session_id)
            callback_handler = AgentCallbackHandler()
            
            # Send initial event
            yield f"data: {json.dumps({'type': 'start', 'message': 'Processing...'})}\n\n"
            
            # Run agent with streaming
            response = await agent.arun(
                request.message,
                callbacks=[callback_handler]
            )
            
            # Stream the response
            for chunk in response.split():
                yield f"data: {json.dumps({'type': 'token', 'content': chunk + ' '})}\n\n"
                await asyncio.sleep(0.01)  # Small delay for streaming effect
            
            # Send tool calls if any
            if callback_handler.tool_calls:
                yield f"data: {json.dumps({'type': 'tools', 'tools': callback_handler.tool_calls})}\n\n"
            
            # Log interaction
            await log_interaction(
                session_id=request.session_id or "default",
                user_message=request.message,
                agent_response=response,
                tools_used=callback_handler.tool_calls
            )
            
            # Send completion event
            yield f"data: {json.dumps({'type': 'end', 'message': 'Complete'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in chat stream: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/tools/run")
async def run_tool(request: ToolRequest):
    """
    Execute a specific tool directly
    """
    try:
        tools = get_available_tools()
        tool = next((t for t in tools if t.name == request.tool_name), None)
        
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool {request.tool_name} not found")
        
        result = await tool.arun(**request.parameters)
        
        return {
            "tool": request.tool_name,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error running tool {request.tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/evals")
async def get_evaluations(limit: int = 100):
    """
    Get evaluation results and metrics
    """
    try:
        evals = await get_evals(limit=limit)
        return {
            "evaluations": evals,
            "total": len(evals)
        }
    except Exception as e:
        logger.error(f"Error fetching evaluations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """
    List all available tools
    """
    tools = get_available_tools()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in tools
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
