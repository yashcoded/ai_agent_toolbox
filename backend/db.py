"""
Database operations for logging and evaluations
"""
import os
import asyncpg
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

# Database connection pool
_db_pool = None


async def get_db_pool():
    """Get or create database connection pool"""
    global _db_pool
    
    if _db_pool is None:
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/ai_agent"
        )
        _db_pool = await asyncpg.create_pool(db_url)
    
    return _db_pool


async def init_db():
    """Initialize database tables"""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        # Create interactions table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255),
                user_message TEXT,
                agent_response TEXT,
                tools_used JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create evaluations table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id SERIAL PRIMARY KEY,
                test_name VARCHAR(255),
                input_text TEXT,
                expected_output TEXT,
                actual_output TEXT,
                passed BOOLEAN,
                score FLOAT,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


async def get_db_connection():
    """Get a database connection from the pool"""
    pool = await get_db_pool()
    return await pool.acquire()


async def log_interaction(
    session_id: str,
    user_message: str,
    agent_response: str,
    tools_used: Optional[List[Dict[str, Any]]] = None
):
    """Log an interaction to the database"""
    try:
        pool = await get_db_pool()
        
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO interactions (session_id, user_message, agent_response, tools_used)
                VALUES ($1, $2, $3, $4)
                """,
                session_id,
                user_message,
                agent_response,
                json.dumps(tools_used or [])
            )
    except Exception as e:
        print(f"Error logging interaction: {e}")


async def log_evaluation(
    test_name: str,
    input_text: str,
    expected_output: str,
    actual_output: str,
    passed: bool,
    score: float,
    metadata: Optional[Dict[str, Any]] = None
):
    """Log an evaluation result"""
    try:
        pool = await get_db_pool()
        
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO evaluations (test_name, input_text, expected_output, actual_output, passed, score, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                test_name,
                input_text,
                expected_output,
                actual_output,
                passed,
                score,
                json.dumps(metadata or {})
            )
    except Exception as e:
        print(f"Error logging evaluation: {e}")


async def get_evals(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve evaluation results"""
    try:
        pool = await get_db_pool()
        
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, test_name, input_text, expected_output, actual_output, 
                       passed, score, metadata, created_at
                FROM evaluations
                ORDER BY created_at DESC
                LIMIT $1
                """,
                limit
            )
            
            return [
                {
                    "id": row["id"],
                    "test_name": row["test_name"],
                    "input_text": row["input_text"],
                    "expected_output": row["expected_output"],
                    "actual_output": row["actual_output"],
                    "passed": row["passed"],
                    "score": row["score"],
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                    "created_at": row["created_at"].isoformat()
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error fetching evaluations: {e}")
        return []


async def get_interaction_history(session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get interaction history for a session"""
    try:
        pool = await get_db_pool()
        
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, user_message, agent_response, tools_used, created_at
                FROM interactions
                WHERE session_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                session_id,
                limit
            )
            
            return [
                {
                    "id": row["id"],
                    "user_message": row["user_message"],
                    "agent_response": row["agent_response"],
                    "tools_used": json.loads(row["tools_used"]) if row["tools_used"] else [],
                    "created_at": row["created_at"].isoformat()
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error fetching interaction history: {e}")
        return []
