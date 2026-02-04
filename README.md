# AI Agent Toolbox 🤖

A comprehensive AI agent system built with LangChain, FastAPI, and Next.js featuring streaming agents, tool calling, evaluations, and observability.

## Features ✨

- **🤖 Multiple AI Agents**: Research and Code agents with specialized capabilities
- **🔧 Tool Registry**: Extensible tool system with calculator, search, and code analysis
- **📡 SSE Streaming**: Real-time streaming responses from agents
- **📊 Evaluation Framework**: Comprehensive testing and scoring system
- **📈 Observability**: PostgreSQL metrics and Redis caching
- **🎨 Modern UI**: Next.js dashboard with chat, tool visualizer, and eval dashboard
- **🐳 Docker Ready**: Complete containerized setup with docker-compose
- **🔄 CI/CD**: GitHub Actions workflow for automated testing

## Architecture

```
ai-agent-toolbox/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── agents/      # LangChain agents (Research, Code)
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration
│   │   ├── db/          # Database session management
│   │   ├── models/      # SQLAlchemy models
│   │   ├── services/    # Redis and other services
│   │   └── tools/       # Tool registry and implementations
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Next.js app router
│   │   └── components/ # React components
│   └── package.json
├── tests/              # Test suites
├── docker-compose.yml  # Docker orchestration
└── .github/workflows/  # CI/CD pipelines
```

## Prerequisites 📋

- Docker and Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+
  - Redis 7+

## Quick Start with Docker 🚀

1. **Clone the repository**
```bash
git clone https://github.com/yashcoded/ai_agent_toolbox.git
cd ai_agent_toolbox
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Manual Setup (Without Docker) 🛠️

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp ../.env.example .env
# Edit .env with your configuration
```

5. **Start PostgreSQL and Redis**
```bash
# Using Docker for databases only
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

6. **Run the backend**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

4. **Open your browser**
```bash
http://localhost:3000
```

## API Endpoints 📡

### Agents
- `POST /api/agents/run` - Run an agent with a query
- `POST /api/agents/stream` - Stream agent responses (SSE)
- `GET /api/agents/history` - Get agent execution history

### Tools
- `GET /api/tools/list` - List all available tools
- `GET /api/tools/{tool_name}` - Get tool details

### Evaluations
- `POST /api/evals/run` - Run evaluation tests
- `GET /api/evals/history` - Get evaluation history

### Metrics
- `GET /api/metrics/overview` - Get system metrics overview
- `GET /api/metrics/agent-stats` - Get agent statistics

## Usage Examples 💡

### Running a Research Agent
```python
import requests

response = requests.post('http://localhost:8000/api/agents/run', json={
    'query': 'What is machine learning?',
    'agent_type': 'research',
    'stream': False
})
print(response.json()['response'])
```

### Running Evaluations
```python
import requests

response = requests.post('http://localhost:8000/api/evals/run', json={
    'eval_name': 'math_eval',
    'agent_type': 'research',
    'test_cases': [
        {'test_case': 'What is 2+2?', 'expected': '4'},
        {'test_case': 'What is 10*5?', 'expected': '50'}
    ]
})
print(response.json())
```

### Streaming Agent Responses
```javascript
const eventSource = new EventSource('http://localhost:8000/api/agents/stream?query=hello');
eventSource.onmessage = (event) => {
    console.log(JSON.parse(event.data));
};
```

## Running Tests 🧪

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Build
```bash
cd frontend
npm run build
npm run lint
```

## Development 👨‍💻

### Adding New Tools

1. Edit `backend/app/tools/registry.py`
2. Add your tool to the `_register_default_tools` method:

```python
my_tool = Tool(
    name="my_tool",
    description="Description of what the tool does",
    func=self._my_tool_function,
)
self.register_tool(my_tool, ["research", "code"])
```

### Adding New Agents

1. Create a new file in `backend/app/agents/`
2. Implement your agent class following the existing patterns
3. Register it in `backend/app/api/agents.py`

### Customizing Prompts

Edit the system prompts in:
- `backend/app/agents/research_agent.py`
- `backend/app/agents/code_agent.py`

## Database Schema 💾

### Tables
- **agent_runs**: Tracks agent executions
- **tool_calls**: Records tool usage
- **evaluations**: Stores evaluation results
- **prompt_versions**: Manages prompt versioning

## Configuration ⚙️

Key configuration options in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DEFAULT_MODEL`: LLM model to use (default: gpt-4-turbo-preview)
- `TEMPERATURE`: Model temperature (default: 0.7)
- `MAX_ITERATIONS`: Maximum agent iterations (default: 10)
- `POSTGRES_*`: PostgreSQL connection settings
- `REDIS_*`: Redis connection settings

## Monitoring & Observability 📊

### Metrics Dashboard
Access the evaluation dashboard at http://localhost:3000 to view:
- Total agent runs
- Average execution duration
- Tool call statistics
- Evaluation results and scores

### Database Metrics
All agent runs, tool calls, and evaluations are stored in PostgreSQL for analysis.

### Redis Caching
Redis is used for:
- Agent conversation memory
- Caching frequently accessed data
- Session management

## Troubleshooting 🔧

### Common Issues

**Backend fails to start:**
- Ensure PostgreSQL and Redis are running
- Check database connection settings in `.env`
- Verify OpenAI API key is set

**Frontend can't connect to backend:**
- Verify backend is running on port 8000
- Check CORS settings in `backend/app/core/config.py`

**Agent requests fail:**
- Verify OpenAI API key is valid and has credits
- Check agent type is either 'research' or 'code'

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at http://localhost:8000/docs

## Roadmap 🗺️

- [ ] Add more agent types (Data Analysis, Writing, etc.)
- [ ] Implement vector database for semantic search
- [ ] Add authentication and user management
- [ ] Expand evaluation framework
- [ ] Add more built-in tools
- [ ] Implement agent orchestration
- [ ] Add monitoring dashboards (Grafana)
- [ ] Support for multiple LLM providers

---

Built with ❤️ using LangChain, FastAPI, and Next.js