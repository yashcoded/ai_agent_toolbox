"""
LangChain agent implementation with tool calling
"""
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Optional
import os
import redis
import json

# Try relative import first, then absolute
try:
    from .tools import get_available_tools
except ImportError:
    from tools import get_available_tools


# Redis client for memory
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


class AgentCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for streaming and logging"""
    
    def __init__(self):
        self.tool_calls = []
        self.tokens = []
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        """Called when tool starts"""
        tool_name = serialized.get("name", "unknown")
        self.tool_calls.append({
            "name": tool_name,
            "input": input_str,
            "status": "started"
        })
    
    def on_tool_end(self, output: str, **kwargs):
        """Called when tool ends"""
        if self.tool_calls:
            self.tool_calls[-1]["output"] = output
            self.tool_calls[-1]["status"] = "completed"
    
    def on_llm_new_token(self, token: str, **kwargs):
        """Called when LLM generates a new token"""
        self.tokens.append(token)


def load_master_prompt() -> str:
    """Load the master prompt from file"""
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "master_prompt.txt")
    try:
        with open(prompt_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        # Default prompt if file not found
        return "You are a production AI agent. Use tools when needed, reason step by step, return concise answers, log actions, and prefer reliable sources."


def create_agent(session_id: Optional[str] = None) -> AgentExecutor:
    """
    Create a LangChain agent with tool calling capabilities
    """
    # Load master prompt
    master_prompt = load_master_prompt()
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", master_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Get tools
    tools = get_available_tools()
    
    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Load memory from Redis if session_id provided
    memory = None
    if session_id:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        # Try to load previous conversation
        try:
            history = redis_client.get(f"session:{session_id}")
            if history:
                memory.chat_memory.messages = json.loads(history)
        except Exception as e:
            print(f"Error loading memory: {e}")
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    return agent_executor


def save_memory(session_id: str, memory: ConversationBufferMemory):
    """Save conversation memory to Redis"""
    try:
        messages_json = json.dumps([msg.dict() for msg in memory.chat_memory.messages])
        redis_client.setex(f"session:{session_id}", 3600, messages_json)  # 1 hour TTL
    except Exception as e:
        print(f"Error saving memory: {e}")
