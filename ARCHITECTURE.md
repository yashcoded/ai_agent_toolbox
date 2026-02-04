# Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                       │
│  ┌───────────────┐  ┌──────────────┐  ┌───────────────────┐    │
│  │ Chat Interface│  │Tool Visualizer│  │ Eval Dashboard   │    │
│  └───────┬───────┘  └──────┬───────┘  └────────┬─────────┘    │
│          │                  │                    │               │
│          └──────────────────┼────────────────────┘               │
│                             │                                    │
│                      ┌──────▼────────┐                          │
│                      │   API Client   │                          │
│                      └──────┬────────┘                          │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                    HTTP/SSE  │
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    API Layer                            │    │
│  │  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐  │    │
│  │  │  Agents  │  │  Tools   │  │ Evals  │  │ Metrics │  │    │
│  │  │  Router  │  │  Router  │  │ Router │  │ Router  │  │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬───┘  └────┬────┘  │    │
│  └───────┼─────────────┼─────────────┼───────────┼────────┘    │
│          │             │             │           │              │
│  ┌───────▼─────────────▼─────────────▼───────────▼────────┐    │
│  │                  Business Logic                         │    │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │   Agents    │  │Tool Registry │  │   Services   │  │    │
│  │  │ ┌─────────┐ │  │              │  │              │  │    │
│  │  │ │Research │ │  │  - Calculator│  │  - Redis     │  │    │
│  │  │ │  Agent  │ │  │  - Search    │  │  - Metrics   │  │    │
│  │  │ └─────────┘ │  │  - Code      │  │              │  │    │
│  │  │ ┌─────────┐ │  │    Analyzer  │  │              │  │    │
│  │  │ │  Code   │ │  │              │  │              │  │    │
│  │  │ │  Agent  │ │  │              │  │              │  │    │
│  │  │ └─────────┘ │  │              │  │              │  │    │
│  │  └─────────────┘  └──────────────┘  └──────────────┘  │    │
│  └──────┬────────────────────┬───────────────┬────────────┘    │
│         │                    │               │                  │
│  ┌──────▼────────┐    ┌──────▼──────┐  ┌────▼────────┐       │
│  │   LangChain   │    │  Database   │  │   Redis     │       │
│  │   (OpenAI)    │    │   (Models)  │  │  (Cache)    │       │
│  └───────────────┘    └──────┬──────┘  └────┬────────┘       │
└────────────────────────────────┼─────────────┼─────────────────┘
                                 │             │
                    ┌────────────▼─────────────▼────────────┐
                    │        Infrastructure                  │
                    │  ┌──────────────┐  ┌──────────────┐  │
                    │  │  PostgreSQL  │  │    Redis     │  │
                    │  │              │  │              │  │
                    │  │ - AgentRuns  │  │ - Sessions   │  │
                    │  │ - ToolCalls  │  │ - Cache      │  │
                    │  │ - Evals      │  │ - Memory     │  │
                    │  │ - Prompts    │  │              │  │
                    │  └──────────────┘  └──────────────┘  │
                    └─────────────────────────────────────┘
```

## Component Interactions

### Agent Execution Flow

```
User Query → Chat Interface → API Client → /api/agents/run
                                              │
                                              ▼
                                        Agent Router
                                              │
                                              ▼
                                     Select Agent Type
                                    (Research or Code)
                                              │
                                              ▼
                                        Agent Executor
                                              │
                        ┌─────────────────────┼─────────────────────┐
                        │                     │                     │
                        ▼                     ▼                     ▼
                  LangChain LLM         Tool Registry         Redis Cache
                        │                     │                     │
                        │              ┌──────▼──────┐             │
                        │              │  - Calculator│             │
                        │              │  - Search    │             │
                        │              │  - Code      │             │
                        │              └──────┬──────┘             │
                        │                     │                     │
                        └─────────────────────┼─────────────────────┘
                                              │
                                              ▼
                                     Store in PostgreSQL
                                    (AgentRuns, ToolCalls)
                                              │
                                              ▼
                                      Return Response
```

### Streaming Flow (SSE)

```
User Query → Chat Interface → EventSource → /api/agents/stream
                                                    │
                                                    ▼
                                            Agent.astream()
                                                    │
                                    ┌───────────────┴────────────────┐
                                    │                                │
                                    ▼                                ▼
                            Chunk Processing                  SSE Response
                                    │                                │
                                    └────────────────┬───────────────┘
                                                     │
                                                     ▼
                                            Frontend Updates
                                            (Real-time UI)
```

## Data Models

### PostgreSQL Schema

```
agent_runs
├── id (PK)
├── agent_type
├── prompt
├── response
├── tools_used (JSON)
├── duration_ms
├── status
├── created_at
└── metadata (JSON)

tool_calls
├── id (PK)
├── run_id (FK)
├── tool_name
├── input_data (JSON)
├── output_data (JSON)
├── duration_ms
├── success
└── created_at

evaluations
├── id (PK)
├── eval_name
├── agent_type
├── test_case
├── expected
├── actual
├── score
├── passed
├── created_at
└── metadata (JSON)

prompt_versions
├── id (PK)
├── name
├── version
├── template
├── variables (JSON)
├── is_active
├── created_at
└── metadata (JSON)
```
