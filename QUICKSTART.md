# Quick Start Guide

Get AI Agent Toolbox running in 5 minutes! 🚀

## Prerequisites

Choose one of the following setups:

**Option A: Docker (Recommended)**
- Docker Desktop or Docker Engine + Docker Compose
- Your OpenAI API key

**Option B: Local Development**
- Python 3.11+
- Node.js 18+
- Your OpenAI API key

## 🚀 Quick Start with Docker (Easiest)

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/yashcoded/ai_agent_toolbox.git
cd ai_agent_toolbox

# Create environment file
cp .env.example .env
```

### Step 2: Add Your OpenAI API Key

Edit `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Start Everything

```bash
docker-compose up -d
```

That's it! 🎉

### Step 4: Access the Application

- **Frontend (UI):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Step 5: Try It Out

1. Open http://localhost:3000 in your browser
2. Select "Research Agent"
3. Type a question like "What is machine learning?"
4. Click "Send" and watch the AI respond!

## 📊 What You Can Do Now

### Chat with AI Agents
1. Go to the **Chat** tab
2. Choose between Research or Code agent
3. Ask questions or request code

### View Available Tools
1. Go to the **Tools** tab
2. See all tools available to agents
3. Understand what each tool does

### Run Evaluations
1. Go to the **Evaluations** tab
2. View evaluation metrics
3. See pass/fail rates

## 🛠️ Local Development (Without Docker)

If you prefer not to use Docker:

### Step 1: Clone and Configure

```bash
git clone https://github.com/yashcoded/ai_agent_toolbox.git
cd ai_agent_toolbox
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Step 2: Use the Start Script

```bash
chmod +x start-dev.sh
./start-dev.sh
```

The script will:
- Start PostgreSQL and Redis in Docker
- Set up Python virtual environment
- Install backend dependencies
- Start FastAPI backend on port 8000
- Install frontend dependencies
- Start Next.js frontend on port 3000

Press `Ctrl+C` to stop all services.

## 📚 Next Steps

### Learn More
- Read the full [README.md](README.md)
- Check [API_EXAMPLES.md](API_EXAMPLES.md) for API usage
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design

### Customize
- Add your own tools in `backend/app/tools/registry.py`
- Create new agents in `backend/app/agents/`
- Modify prompts in agent files

### Test
```bash
# Run backend tests
cd backend
pytest tests/ -v

# Build frontend
cd frontend
npm run build
```

## 🐛 Troubleshooting

### Port Already in Use
If ports 3000, 8000, 5432, or 6379 are in use:

**For Docker:**
```bash
docker-compose down
# Edit docker-compose.yml to change port mappings
docker-compose up -d
```

**For Local:**
```bash
# Stop the conflicting services or change ports in configuration
```

### Backend Won't Start
- Ensure PostgreSQL and Redis are running
- Check your `.env` file has correct database settings
- Verify your OpenAI API key is valid

### Frontend Won't Connect
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS settings in `backend/app/core/config.py`

### Database Connection Error
```bash
# Restart database containers
docker restart ai_agent_postgres ai_agent_redis

# Or recreate them
docker-compose down
docker-compose up -d
```

## 🔧 Development Commands

### Using Make
```bash
make help          # Show all commands
make dev-up        # Start with Docker
make dev-down      # Stop all services
make test          # Run tests
make clean         # Clean temporary files
```

### Manual Commands

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Tests:**
```bash
cd backend
pytest tests/ -v
```

## 🎯 Example API Calls

### Run an Agent
```bash
curl -X POST http://localhost:8000/api/agents/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Python?",
    "agent_type": "research"
  }'
```

### List Tools
```bash
curl http://localhost:8000/api/tools/list
```

### Get Metrics
```bash
curl http://localhost:8000/api/metrics/overview
```

## 🔑 Getting an OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key to your `.env` file

**Important:** Keep your API key secret and never commit it to version control!

## 📞 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bugs or questions
- Check the API docs at http://localhost:8000/docs

## ✅ Verification Checklist

After starting the application, verify everything works:

- [ ] Frontend loads at http://localhost:3000
- [ ] Backend API responds at http://localhost:8000
- [ ] API docs load at http://localhost:8000/docs
- [ ] Can send a message in the chat interface
- [ ] Tools list shows available tools
- [ ] Metrics dashboard displays data
- [ ] No errors in browser console
- [ ] No errors in terminal/logs

If all items are checked, you're ready to go! 🎉

---

**Enjoy building with AI Agent Toolbox!** 🤖✨
