.PHONY: help install dev-up dev-down build test clean

help:
	@echo "AI Agent Toolbox - Available commands:"
	@echo "  make install    - Install all dependencies"
	@echo "  make dev-up     - Start all services with Docker Compose"
	@echo "  make dev-down   - Stop all services"
	@echo "  make build      - Build all Docker images"
	@echo "  make test       - Run all tests"
	@echo "  make clean      - Clean up temporary files"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

dev-up:
	@echo "Starting all services..."
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

dev-down:
	@echo "Stopping all services..."
	docker-compose down

build:
	@echo "Building Docker images..."
	docker-compose build

test:
	@echo "Running backend tests..."
	cd backend && pytest tests/ -v
	@echo "Building frontend..."
	cd frontend && npm run build

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf frontend/node_modules
	rm -rf frontend/.next
	rm -rf backend/venv
