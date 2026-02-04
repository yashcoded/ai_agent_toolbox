"""Database models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class AgentRun(Base):
    """Model for agent execution runs."""
    
    __tablename__ = "agent_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text)
    tools_used = Column(JSON)
    duration_ms = Column(Float)
    status = Column(String(20), default="running")
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)


class ToolCall(Base):
    """Model for tool execution tracking."""
    
    __tablename__ = "tool_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, index=True)
    tool_name = Column(String(100), nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    duration_ms = Column(Float)
    success = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class Evaluation(Base):
    """Model for evaluation results."""
    
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    eval_name = Column(String(100), nullable=False)
    agent_type = Column(String(50))
    test_case = Column(Text)
    expected = Column(Text)
    actual = Column(Text)
    score = Column(Float)
    passed = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)


class PromptVersion(Base):
    """Model for prompt versioning."""
    
    __tablename__ = "prompt_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    version = Column(Integer, nullable=False)
    template = Column(Text, nullable=False)
    variables = Column(JSON)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)
