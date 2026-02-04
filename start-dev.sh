#!/bin/bash

# AI Agent Toolbox - Local Development Startup Script

set -e

echo "🚀 Starting AI Agent Toolbox Development Environment"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    read -p "Press enter to continue..."
fi

# Start PostgreSQL and Redis with Docker
echo "🐳 Starting PostgreSQL and Redis..."
docker run -d --name ai_agent_postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=ai_agent_toolbox \
    -p 5432:5432 \
    postgres:15-alpine 2>/dev/null || docker start ai_agent_postgres

docker run -d --name ai_agent_redis \
    -p 6379:6379 \
    redis:7-alpine 2>/dev/null || docker start ai_agent_redis

sleep 3

echo "✅ Databases started"
echo ""

# Start backend in background
echo "🔧 Starting FastAPI backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Start frontend
echo "⚛️  Starting Next.js frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 AI Agent Toolbox is running!"
echo ""
echo "📱 Frontend:  http://localhost:3000"
echo "🔌 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; docker stop ai_agent_postgres ai_agent_redis; echo '✅ All services stopped'; exit 0" INT

wait
