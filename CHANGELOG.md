# Changelog

All notable changes to the AI Agent Toolbox project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2024

### Security
- Updated Next.js from 15.0.8 to 15.2.3 to fix additional vulnerabilities:
  - DoS via cache poisoning (patched in 15.1.8)
  - Authorization bypass in Next.js Middleware (patched in 15.2.3)

## [0.1.2] - 2024

### Security
- Updated Next.js from 14.2.35 to 15.0.8 to fix additional HTTP request deserialization DoS vulnerability affecting React Server Components

## [0.1.1] - 2024

### Security
- Updated fastapi from 0.109.0 to 0.109.1 to fix ReDoS vulnerability
- Updated langchain-community from 0.0.13 to 0.3.27 to fix:
  - XML External Entity (XXE) Attacks vulnerability
  - SSRF vulnerability in RequestsToolkit component
  - Pickle deserialization of untrusted data vulnerability
- Updated python-multipart from 0.0.6 to 0.0.22 to fix:
  - Arbitrary File Write via Non-Default Configuration
  - Denial of service (DoS) via deformation multipart/form-data boundary
  - Content-Type Header ReDoS vulnerability
- Updated Next.js from 14.1.0 to 14.2.35 to fix:
  - HTTP request deserialization DoS vulnerabilities
  - Authorization bypass vulnerability
  - Cache poisoning vulnerability
  - Server-Side Request Forgery (SSRF) in Server Actions
  - Authorization Bypass in Middleware

## [0.1.0] - 2024

### Added

#### Backend
- FastAPI application with async support
- LangChain integration for AI agents
- Research Agent for information gathering and analysis
- Code Agent for code generation and analysis
- Tool Registry system for managing agent tools
- SSE (Server-Sent Events) streaming endpoints
- PostgreSQL integration for metrics storage
  - AgentRuns table for execution tracking
  - ToolCalls table for tool usage tracking
  - Evaluations table for test results
  - PromptVersions table for prompt management
- Redis integration for caching and memory
- RESTful API endpoints:
  - `/api/agents/run` - Execute agents
  - `/api/agents/stream` - Stream agent responses
  - `/api/agents/history` - View execution history
  - `/api/tools/list` - List available tools
  - `/api/tools/{name}` - Get tool details
  - `/api/evals/run` - Run evaluations
  - `/api/evals/history` - View evaluation history
  - `/api/metrics/overview` - Get system metrics
  - `/api/metrics/agent-stats` - Get agent statistics
- Default tools:
  - Calculator tool
  - Search tool (mock)
  - Code analyzer tool
- Comprehensive error handling
- CORS middleware configuration
- Health check endpoint

#### Frontend
- Next.js 14 application with App Router
- TypeScript support
- Tailwind CSS for styling
- Three main components:
  - ChatInterface - Real-time chat with agents
  - ToolVisualizer - Display available tools
  - EvalDashboard - Metrics and evaluation results
- Tab-based navigation
- Responsive design
- Real-time agent streaming support
- API client utilities
- Chart visualization with Recharts

#### Infrastructure
- Docker support with multi-container setup
  - Backend container (Python/FastAPI)
  - Frontend container (Node/Next.js)
  - PostgreSQL container
  - Redis container
- Docker Compose orchestration
- Volume persistence for databases
- Health checks for all services
- Development environment scripts
  - `start-dev.sh` for local development
  - Makefile with common commands

#### Testing
- Pytest configuration for backend
- Async test support
- Test fixtures and utilities
- API endpoint tests
- CI/CD pipeline with GitHub Actions
  - Backend tests workflow
  - Frontend build workflow
  - Docker build verification

#### Documentation
- Comprehensive README with:
  - Feature overview
  - Architecture description
  - Quick start guide
  - Installation instructions
  - Usage examples
- ARCHITECTURE.md with system diagrams
- API_EXAMPLES.md with code examples in multiple languages
- CONTRIBUTING.md with contribution guidelines
- QUICKSTART.md for rapid setup
- CHANGELOG.md (this file)
- Inline code documentation

#### Configuration
- Environment variable support via .env
- Configurable settings:
  - Database connections
  - Redis configuration
  - OpenAI API settings
  - CORS origins
  - Agent parameters (model, temperature, max iterations)
- .env.example template
- .gitignore for Python and Node.js
- ESLint configuration for frontend
- Pytest configuration

### Dependencies

#### Backend
- fastapi==0.109.0
- uvicorn==0.27.0
- langchain==0.1.0
- langchain-openai==0.0.5
- sqlalchemy==2.0.25
- asyncpg==0.29.0
- redis==5.0.1
- pydantic-settings==2.1.0
- sse-starlette==1.8.2
- pytest==7.4.4

#### Frontend
- next==14.1.0
- react==18.2.0
- typescript==5.3.3
- tailwindcss==3.4.1
- axios==1.6.5
- recharts==2.12.0
- lucide-react==0.312.0

### Project Structure
```
ai-agent-toolbox/
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── tests/               # Test suites
├── .github/workflows/   # CI/CD
├── docker-compose.yml   # Docker orchestration
├── Dockerfile.backend   # Backend container
├── Dockerfile.frontend  # Frontend container
└── Documentation files
```

## [Unreleased]

### Planned Features
- [ ] Authentication and authorization
- [ ] User management system
- [ ] More agent types (Data Analysis, Writing, etc.)
- [ ] Vector database integration
- [ ] Advanced tool marketplace
- [ ] Multi-LLM provider support
- [ ] Monitoring dashboards (Grafana/Prometheus)
- [ ] Webhook support
- [ ] Agent orchestration and workflows
- [ ] Conversation memory persistence
- [ ] Cost tracking and budgeting
- [ ] Role-based access control

### Known Issues
- Agent responses require valid OpenAI API key
- Streaming may not work in all browsers
- Limited error messages for failed tool executions
- No authentication/authorization (local use only)

## Version History

- **0.1.0** - Initial release with core functionality

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
