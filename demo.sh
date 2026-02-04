#!/bin/bash

# AI Agent Toolbox Demo Script
# This script demonstrates the key features of the AI Agent Toolbox

echo "🤖 AI Agent Toolbox Demo"
echo "========================="
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

echo "📦 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ Services are running!"
echo ""
echo "📍 Available endpoints:"
echo "   - Frontend:  http://localhost:3000"
echo "   - Backend:   http://localhost:8000"
echo "   - API Docs:  http://localhost:8000/docs"
echo "   - Evals:     http://localhost:3000/evals"
echo ""
echo "🧪 Testing backend health..."
curl -s http://localhost:8000/ | python3 -m json.tool

echo ""
echo "🛠️  Available tools:"
curl -s http://localhost:8000/tools | python3 -m json.tool

echo ""
echo "📝 Try these example queries in the chat UI:"
echo "   1. 'What is 25 * 48?'"
echo "   2. 'Search for the latest news about artificial intelligence'"
echo "   3. 'Write Python code to calculate fibonacci(10)'"
echo ""
echo "🎉 Demo complete! Press Ctrl+C to stop the services when done."
echo ""

# Keep the script running
docker-compose logs -f
