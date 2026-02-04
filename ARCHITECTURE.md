# AI Agent Toolbox - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Frontend (Next.js)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Chat UI      │  │ Tool         │  │ Evaluation Dashboard     │  │
│  │ (SSE Stream) │  │ Visualizer   │  │ (Metrics & Results)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│         │                  │                      │                  │
└─────────┼──────────────────┼──────────────────────┼──────────────────┘
          │                  │                      │
          │                  │                      │
          │ HTTP/SSE         │ REST API             │ REST API
          ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Backend (FastAPI)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ /chat/stream │  │ /tools/run   │  │ /evals                   │  │
│  │ (SSE)        │  │              │  │                          │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│         │                  │                      │                  │
│         └──────────────────┼──────────────────────┘                  │
│                            │                                         │
│                    ┌───────▼────────┐                                │
│                    │  LangChain     │                                │
│                    │  Agent         │                                │
│                    └───────┬────────┘                                │
│                            │                                         │
│         ┌──────────────────┼──────────────────┐                     │
│         │                  │                  │                     │
│    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐               │
│    │web_     │      │calculator │     │code_exec  │               │
│    │search   │      │           │     │           │               │
│    └─────────┘      └───────────┘     └───────────┘               │
└─────────────────────────────────────────────────────────────────────┘
          │                                         │
          │                                         │
          ▼                                         ▼
┌──────────────────┐                    ┌──────────────────────┐
│  Redis           │                    │  PostgreSQL          │
│  (Session        │                    │  (Logs & Evals)      │
│   Memory)        │                    │                      │
└──────────────────┘                    └──────────────────────┘
```

## Data Flow

### Chat Stream Flow
1. User sends message via frontend
2. Frontend calls `/chat/stream` endpoint with SSE
3. Backend creates/retrieves agent with session ID
4. Agent processes message, calling tools as needed
5. Response streams back as tokens via SSE
6. Session memory saved to Redis
7. Interaction logged to PostgreSQL

### Tool Execution Flow
1. Agent determines which tool to use
2. Tool function executes (web_search, calculator, or code_exec)
3. Tool result returned to agent
4. Agent incorporates result into response
5. Tool usage tracked and displayed in UI

### Evaluation Flow
1. Load test dataset from JSON
2. Run agent on each test case
3. Compare output against expected results
4. Calculate score and pass/fail status
5. Store results in PostgreSQL
6. Display metrics in dashboard

## Components

### Backend Services
- **main.py**: FastAPI application with REST endpoints
- **agent.py**: LangChain agent configuration and setup
- **tools.py**: Tool implementations (web_search, calculator, code_exec)
- **db.py**: Database operations for PostgreSQL
- **evals.py**: Evaluation framework and dataset processing

### Frontend Services
- **ChatInterface.tsx**: Real-time chat UI with SSE streaming
- **ToolVisualizer.tsx**: Display active tool usage
- **evals.tsx**: Evaluation dashboard with metrics
- **api.ts**: API client with SSE support and error handling

### Infrastructure
- **Redis**: Session-based conversation memory (1 hour TTL)
- **PostgreSQL**: Persistent storage for logs and evaluations
- **Docker**: Containerized services with docker-compose

## Key Features

### Streaming Response
- Server-Sent Events (SSE) for real-time token streaming
- Callback handlers for tool execution tracking
- Retry logic and connection management

### Memory Management
- Redis for fast session storage
- Conversation history with 1-hour TTL
- Session ID-based retrieval

### Tool Calling
- Dynamic tool selection by LangChain agent
- Three built-in tools with extensible framework
- Safe execution with timeouts and sandboxing

### Evaluation System
- JSON-based test datasets
- Automated scoring with keyword matching
- Historical tracking in PostgreSQL
- Metrics dashboard for performance monitoring

## Security Considerations

1. **Code Execution**: Sandboxed with 5-second timeout
2. **Calculator**: Sanitized input, no arbitrary code eval
3. **API Keys**: Environment variable based configuration
4. **Database**: Connection pooling with asyncpg
5. **CORS**: Configurable origins in FastAPI middleware

## Scalability

- **Horizontal Scaling**: Stateless backend services
- **Caching**: Redis for session data
- **Database**: PostgreSQL with connection pooling
- **Load Balancing**: Docker services can be replicated

## Monitoring & Logging

- Interaction logging to PostgreSQL
- Tool execution tracking
- Evaluation metrics and dashboards
- Error handling and logging throughout
