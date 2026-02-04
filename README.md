# AI Agent Toolbox

A production-ready AI agent platform with tool calling, memory, and evaluation capabilities. Built with FastAPI, LangChain, Next.js, Redis, and PostgreSQL.

## Features

### Backend
- **FastAPI REST API** with streaming support (Server-Sent Events)
- **LangChain Agent** with intelligent tool calling
- **Three Built-in Tools**:
  - `web_search` - Search the web for current information
  - `calculator` - Perform mathematical calculations
  - `code_exec` - Execute Python code in a sandboxed environment
- **Redis** for conversation memory and session management
- **PostgreSQL** for interaction logs and evaluation results
- **Streaming responses** with real-time token generation
- **Prompt versioning** system in `/prompts` directory

### Frontend
- **Next.js** modern chat interface
- **Real-time streaming** chat with SSE client
- **Tool visualizer** showing active tool usage
- **Evaluation dashboard** with metrics and test results
- **Retry logic** for robust API communication
- **Session management** with localStorage

### DevOps
- **Docker & docker-compose** for easy deployment
- **PostgreSQL** and **Redis** containerized services
- **Environment-based configuration**
- **Health check endpoints**

### Testing & Evaluation
- **Pytest** test suite for agents and tools
- **Sample evaluation dataset** with test cases
- **Automated evaluation framework** with scoring
- **Metrics dashboard** for tracking performance

## Architecture

```
ai_agent_toolbox/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── agent.py         # LangChain agent setup
│   ├── tools.py         # Tool implementations
│   ├── db.py            # Database operations
│   ├── evals.py         # Evaluation framework
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── pages/          # Next.js pages
│   │   ├── index.tsx   # Chat interface
│   │   └── evals.tsx   # Evaluation dashboard
│   ├── components/     # React components
│   │   ├── ChatInterface.tsx
│   │   └── ToolVisualizer.tsx
│   ├── services/       # API clients
│   │   └── api.ts
│   └── package.json
├── prompts/            # Prompt templates
│   └── master_prompt.txt
├── tests/              # Test suite
│   ├── test_agent.py
│   ├── test_tools.py
│   └── sample_eval_dataset.json
├── docker/             # Docker configs
│   └── Dockerfile
├── docker-compose.yml  # Service orchestration
└── demo.sh            # Demo script
```

## Quick Start

### Prerequisites
- Docker and docker-compose
- OpenAI API key
- (Optional) Serper API key for web search

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yashcoded/ai_agent_toolbox.git
cd ai_agent_toolbox
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. **Start all services with Docker**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Evaluation Dashboard: http://localhost:3000/evals

### Run Demo Script

```bash
./demo.sh
```

This will start all services and demonstrate the key features.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Required
OPENAI_API_KEY=sk-...                    # Your OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo               # Model to use
TEMPERATURE=0.7                          # Model temperature

# Optional
SERPER_API_KEY=...                       # For web search functionality

# Database (defaults provided in docker-compose)
REDIS_HOST=localhost
REDIS_PORT=6379
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_agent

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### POST /chat/stream
Stream chat responses with Server-Sent Events (SSE)

**Request:**
```json
{
  "message": "What is 25 * 48?",
  "session_id": "optional-session-id"
}
```

**Response:** SSE stream with events:
- `start` - Processing started
- `token` - Each token as it's generated
- `tools` - Tool calls made during processing
- `end` - Processing complete
- `error` - Error occurred

### POST /tools/run
Execute a specific tool directly

**Request:**
```json
{
  "tool_name": "calculator",
  "parameters": {
    "expression": "25 * 48"
  }
}
```

**Response:**
```json
{
  "tool": "calculator",
  "result": "1200",
  "status": "success"
}
```

### GET /evals
Get evaluation results and metrics

**Response:**
```json
{
  "evaluations": [...],
  "total": 10
}
```

### GET /tools
List all available tools

**Response:**
```json
{
  "tools": [
    {
      "name": "web_search",
      "description": "Search the web for current information..."
    },
    ...
  ]
}
```

## Development

### Running Backend Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Running Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
cd tests
pip install -r requirements.txt
pytest -v
```

### Database Initialization

The database tables are created automatically on first connection. To manually initialize:

```python
from backend.db import init_db
import asyncio

asyncio.run(init_db())
```

## Tools

### Web Search
Search the web for current information using Serper API.
- Requires `SERPER_API_KEY` environment variable
- Falls back to placeholder if API key not provided

### Calculator
Evaluate mathematical expressions safely.
- Supports basic arithmetic: +, -, *, /, ()
- Sandboxed evaluation (no arbitrary code execution)

### Code Executor
Execute Python code in a sandboxed environment.
- 5-second timeout for safety
- Captures stdout and stderr
- Returns execution results or errors

## Evaluation Framework

Run evaluations on your agent:

```python
from backend.evals import run_evaluation, load_eval_dataset

# Load dataset
dataset = load_eval_dataset("tests/sample_eval_dataset.json")

# Run evaluation
results = await run_evaluation(dataset)

# Results are automatically logged to database
```

View results in the evaluation dashboard at http://localhost:3000/evals

## Prompt Versioning

The master prompt is stored in `/prompts/master_prompt.txt`:

```
You are a production AI agent. Use tools when needed, reason step by step, 
return concise answers, log actions, and prefer reliable sources.
```

You can modify this prompt and version it using git. The agent automatically loads the latest version.

## Master Prompt

The current master prompt instructs the agent to:
- Use tools when appropriate
- Reason through problems step by step
- Provide concise, accurate answers
- Log all actions for auditability
- Prefer reliable, authoritative sources

## Docker Deployment

### Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Services

- **backend**: FastAPI application (port 8000)
- **frontend**: Next.js application (port 3000)
- **redis**: Redis cache (port 6379)
- **postgres**: PostgreSQL database (port 5432)

## Troubleshooting

### Backend won't start
- Check if Redis and PostgreSQL are running
- Verify API keys in `.env` file
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend
- Ensure `NEXT_PUBLIC_API_URL` is set correctly
- Check if backend is accessible at http://localhost:8000
- Verify CORS settings in backend

### Tools not working
- Web search requires `SERPER_API_KEY`
- Check OpenAI API key is valid
- Review tool execution logs in backend

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the API documentation at http://localhost:8000/docs

## Roadmap

- [ ] Add more tools (file operations, API calls, etc.)
- [ ] Implement user authentication
- [ ] Add conversation history export
- [ ] Support for multiple LLM providers
- [ ] Advanced evaluation metrics
- [ ] Real-time collaboration features
- [ ] Plugin system for custom tools

---

Built with ❤️ using FastAPI, LangChain, Next.js, Redis, and PostgreSQL