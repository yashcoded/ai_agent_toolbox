"""Metrics API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any

from app.db.session import get_db
from app.models import AgentRun, ToolCall, Evaluation

router = APIRouter()


@router.get("/overview")
async def get_metrics_overview(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Get overview of system metrics."""
    # Total runs
    total_runs_result = await db.execute(select(func.count(AgentRun.id)))
    total_runs = total_runs_result.scalar() or 0
    
    # Average duration
    avg_duration_result = await db.execute(select(func.avg(AgentRun.duration_ms)))
    avg_duration = avg_duration_result.scalar() or 0
    
    # Total tool calls
    total_tools_result = await db.execute(select(func.count(ToolCall.id)))
    total_tools = total_tools_result.scalar() or 0
    
    # Total evaluations
    total_evals_result = await db.execute(select(func.count(Evaluation.id)))
    total_evals = total_evals_result.scalar() or 0
    
    # Average eval score
    avg_score_result = await db.execute(select(func.avg(Evaluation.score)))
    avg_score = avg_score_result.scalar() or 0
    
    return {
        "total_runs": total_runs,
        "average_duration_ms": float(avg_duration) if avg_duration else 0,
        "total_tool_calls": total_tools,
        "total_evaluations": total_evals,
        "average_eval_score": float(avg_score) if avg_score else 0,
    }


@router.get("/agent-stats")
async def get_agent_stats(db: AsyncSession = Depends(get_db)):
    """Get statistics by agent type."""
    from sqlalchemy import select, func
    
    result = await db.execute(
        select(
            AgentRun.agent_type,
            func.count(AgentRun.id).label("count"),
            func.avg(AgentRun.duration_ms).label("avg_duration"),
        ).group_by(AgentRun.agent_type)
    )
    
    stats = result.all()
    
    return [
        {
            "agent_type": stat.agent_type,
            "total_runs": stat.count,
            "average_duration_ms": float(stat.avg_duration) if stat.avg_duration else 0,
        }
        for stat in stats
    ]
