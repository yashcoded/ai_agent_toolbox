"""Evaluation API endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Evaluation
from app.agents.research_agent import ResearchAgent
from app.agents.code_agent import CodeAgent

router = APIRouter()


class EvalTestCase(BaseModel):
    """Test case for evaluation."""
    test_case: str
    expected: str


class EvalRequest(BaseModel):
    """Request for running evaluations."""
    eval_name: str
    agent_type: str
    test_cases: List[EvalTestCase]


class EvalResult(BaseModel):
    """Result of an evaluation."""
    eval_name: str
    total_tests: int
    passed: int
    failed: int
    average_score: float
    results: List[Dict[str, Any]]


@router.post("/run", response_model=EvalResult)
async def run_evaluation(request: EvalRequest, db: AsyncSession = Depends(get_db)):
    """Run evaluation on agent."""
    # Select agent
    if request.agent_type == "research":
        agent = ResearchAgent()
    elif request.agent_type == "code":
        agent = CodeAgent()
    else:
        return {"error": "Invalid agent type"}
    
    results = []
    passed = 0
    total_score = 0.0
    
    for test_case in request.test_cases:
        try:
            # Run agent
            result = await agent.run(test_case.test_case)
            actual = result.get("output", "")
            
            # Simple scoring: check if expected is in actual (can be improved)
            score = 1.0 if test_case.expected.lower() in actual.lower() else 0.0
            is_passed = score >= 0.5
            
            # Store evaluation
            evaluation = Evaluation(
                eval_name=request.eval_name,
                agent_type=request.agent_type,
                test_case=test_case.test_case,
                expected=test_case.expected,
                actual=actual,
                score=score,
                passed=1 if is_passed else 0,
            )
            db.add(evaluation)
            
            results.append({
                "test_case": test_case.test_case,
                "expected": test_case.expected,
                "actual": actual,
                "score": score,
                "passed": is_passed,
            })
            
            if is_passed:
                passed += 1
            total_score += score
            
        except Exception as e:
            results.append({
                "test_case": test_case.test_case,
                "error": str(e),
                "score": 0.0,
                "passed": False,
            })
    
    await db.commit()
    
    return EvalResult(
        eval_name=request.eval_name,
        total_tests=len(request.test_cases),
        passed=passed,
        failed=len(request.test_cases) - passed,
        average_score=total_score / len(request.test_cases) if request.test_cases else 0.0,
        results=results,
    )


@router.get("/history")
async def get_eval_history(
    limit: int = 10,
    eval_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get evaluation history."""
    from sqlalchemy import select, desc
    
    query = select(Evaluation).order_by(desc(Evaluation.created_at)).limit(limit)
    
    if eval_name:
        query = query.where(Evaluation.eval_name == eval_name)
    
    result = await db.execute(query)
    evals = result.scalars().all()
    
    return [
        {
            "id": eval.id,
            "eval_name": eval.eval_name,
            "agent_type": eval.agent_type,
            "score": eval.score,
            "passed": bool(eval.passed),
            "created_at": eval.created_at.isoformat(),
        }
        for eval in evals
    ]
