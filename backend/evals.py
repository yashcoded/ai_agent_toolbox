"""
Evaluation framework for testing agent performance
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import json
import os

# Try relative imports first, then absolute
try:
    from .agent import create_agent
    from .db import log_evaluation
except ImportError:
    from agent import create_agent
    from db import log_evaluation


class EvalResult(BaseModel):
    """Evaluation result model"""
    test_name: str
    input_text: str
    expected_output: str
    actual_output: str
    passed: bool
    score: float
    metadata: Optional[Dict[str, Any]] = None


class EvalDataset(BaseModel):
    """Evaluation dataset model"""
    name: str
    description: str
    test_cases: List[Dict[str, Any]]


async def run_evaluation(dataset: EvalDataset) -> List[EvalResult]:
    """
    Run evaluation on a dataset
    """
    results = []
    agent = create_agent()
    
    for test_case in dataset.test_cases:
        try:
            # Run agent on test input
            actual_output = await agent.arun(test_case["input"])
            
            # Simple evaluation: check if expected keywords are in output
            expected = test_case.get("expected_keywords", [])
            score = sum(1 for keyword in expected if keyword.lower() in actual_output.lower()) / max(len(expected), 1)
            passed = score >= test_case.get("pass_threshold", 0.5)
            
            result = EvalResult(
                test_name=test_case.get("name", "unnamed_test"),
                input_text=test_case["input"],
                expected_output=str(expected),
                actual_output=actual_output,
                passed=passed,
                score=score,
                metadata={
                    "dataset": dataset.name,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # Log to database
            await log_evaluation(
                test_name=result.test_name,
                input_text=result.input_text,
                expected_output=result.expected_output,
                actual_output=result.actual_output,
                passed=result.passed,
                score=result.score,
                metadata=result.metadata
            )
            
            results.append(result)
            
        except Exception as e:
            print(f"Error running test case {test_case.get('name')}: {e}")
    
    return results


def load_eval_dataset(dataset_path: str) -> EvalDataset:
    """Load evaluation dataset from JSON file"""
    with open(dataset_path, "r") as f:
        data = json.load(f)
    return EvalDataset(**data)
