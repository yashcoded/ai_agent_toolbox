"""Agent API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import json
import time

from app.agents.research_agent import ResearchAgent
from app.agents.code_agent import CodeAgent
from app.db.session import get_db
from app.models import AgentRun
from app.services.redis_service import get_redis_client

router = APIRouter()


class AgentRequest(BaseModel):
    """Request model for agent execution."""
    query: str
    agent_type: str = "research"
    stream: bool = False


class AgentResponse(BaseModel):
    """Response model for agent execution."""
    run_id: Optional[int] = None
    agent_type: str
    query: str
    response: str
    tools_used: Optional[list] = []
    duration_ms: float


@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest, db: AsyncSession = Depends(get_db)):
    """Run an agent with the given query."""
    start_time = time.time()
    
    # Select agent
    if request.agent_type == "research":
        agent = ResearchAgent()
    elif request.agent_type == "code":
        agent = CodeAgent()
    else:
        raise HTTPException(status_code=400, detail="Invalid agent type")
    
    try:
        # Run agent
        result = await agent.run(request.query)
        duration_ms = (time.time() - start_time) * 1000
        
        # Store in database
        agent_run = AgentRun(
            agent_type=request.agent_type,
            prompt=request.query,
            response=result.get("output", ""),
            tools_used=result.get("intermediate_steps", []),
            duration_ms=duration_ms,
            status="completed",
        )
        db.add(agent_run)
        await db.commit()
        await db.refresh(agent_run)
        
        return AgentResponse(
            run_id=agent_run.id,
            agent_type=request.agent_type,
            query=request.query,
            response=result.get("output", ""),
            tools_used=[],
            duration_ms=duration_ms,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_agent(request: AgentRequest):
    """Stream agent responses using SSE."""
    if request.agent_type == "research":
        agent = ResearchAgent()
    elif request.agent_type == "code":
        agent = CodeAgent()
    else:
        raise HTTPException(status_code=400, detail="Invalid agent type")
    
    async def event_generator():
        """Generate SSE events."""
        try:
            async for chunk in agent.stream(request.query):
                # Format as SSE
                data = json.dumps(chunk)
                yield f"data: {data}\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
        finally:
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.get("/history")
async def get_agent_history(
    limit: int = 10,
    agent_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get agent execution history."""
    from sqlalchemy import select, desc
    
    query = select(AgentRun).order_by(desc(AgentRun.created_at)).limit(limit)
    
    if agent_type:
        query = query.where(AgentRun.agent_type == agent_type)
    
    result = await db.execute(query)
    runs = result.scalars().all()
    
    return [
        {
            "id": run.id,
            "agent_type": run.agent_type,
            "prompt": run.prompt[:100] + "..." if len(run.prompt) > 100 else run.prompt,
            "status": run.status,
            "duration_ms": run.duration_ms,
            "created_at": run.created_at.isoformat(),
        }
        for run in runs
    ]
