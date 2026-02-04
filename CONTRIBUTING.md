# Contributing to AI Agent Toolbox

Thank you for your interest in contributing to AI Agent Toolbox! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Create a new issue with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend && pytest tests/ -v
   
   # Frontend build
   cd frontend && npm run build
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```
   Use conventional commits:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots for UI changes

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional but recommended)

### Local Development

1. Clone your fork
   ```bash
   git clone https://github.com/your-username/ai_agent_toolbox.git
   cd ai_agent_toolbox
   ```

2. Set up environment
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start development environment
   ```bash
   # Option 1: Docker (recommended)
   docker-compose up -d
   
   # Option 2: Local
   ./start-dev.sh
   ```

## Code Style Guidelines

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

Example:
```python
def process_agent_query(query: str, agent_type: str) -> Dict[str, Any]:
    """
    Process an agent query and return the response.
    
    Args:
        query: The user's query string
        agent_type: Type of agent ('research' or 'code')
    
    Returns:
        Dictionary containing the agent's response
    """
    # Implementation
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow Airbnb style guide
- Use functional components with hooks
- Prefer const over let

Example:
```typescript
interface AgentResponse {
  response: string;
  toolsUsed: string[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  
  // Implementation
};
```

### General

- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Use meaningful variable names

## Testing Guidelines

### Backend Tests

- Write tests for all new API endpoints
- Test both success and error cases
- Use pytest fixtures for common setup
- Aim for >80% code coverage

Example:
```python
@pytest.mark.asyncio
async def test_agent_run():
    """Test agent run endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/agents/run",
            json={"query": "test", "agent_type": "research"},
        )
        assert response.status_code == 200
```

### Frontend Tests

- Test component rendering
- Test user interactions
- Test API integration

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for architectural changes
- Add inline documentation for complex code
- Update API documentation in docstrings

## Adding New Features

### Adding a New Agent

1. Create agent file: `backend/app/agents/your_agent.py`
2. Implement agent class following existing patterns
3. Register in `backend/app/api/agents.py`
4. Add tests
5. Update documentation

### Adding a New Tool

1. Add tool to `backend/app/tools/registry.py`
2. Implement tool function
3. Register for appropriate agent types
4. Add tests
5. Update documentation

### Adding a New UI Component

1. Create component in `frontend/src/components/`
2. Follow TypeScript and React best practices
3. Style with Tailwind CSS
4. Add to appropriate page
5. Update documentation

## Project Structure

```
ai-agent-toolbox/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── agents/      # Agent implementations
│   │   ├── api/         # API routers
│   │   ├── core/        # Core configuration
│   │   ├── db/          # Database
│   │   ├── models/      # Data models
│   │   ├── services/    # Services (Redis, etc.)
│   │   └── tools/       # Tool registry
│   └── tests/           # Backend tests
├── frontend/            # Next.js frontend
│   └── src/
│       ├── app/        # Next.js pages
│       ├── components/ # React components
│       └── lib/        # Utilities
└── tests/              # Integration tests
```

## Review Process

1. All PRs require review before merging
2. Address reviewer feedback promptly
3. Keep PRs focused and reasonably sized
4. Ensure CI tests pass

## Getting Help

- Open an issue for questions
- Check existing documentation
- Review closed issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
