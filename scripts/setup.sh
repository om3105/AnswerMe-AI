#!/usr/bin/env bash
# ==============================
# AnswerMe AI — Development Setup Script
# ==============================
# This script sets up the local development environment.
# Usage: ./scripts/setup.sh

set -euo pipefail

echo "🚀 AnswerMe AI — Development Setup"
echo "=================================="

# Check prerequisites
echo ""
echo "📋 Checking prerequisites..."

command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed."; exit 1; }

echo "✅ All prerequisites met"

# Create .env from example if not exists
echo ""
echo "📝 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env from .env.example"
    echo "⚠️  Please review and update .env with your values"
else
    echo "ℹ️  .env already exists, skipping"
fi

# Build and start containers
echo ""
echo "🐳 Building and starting Docker containers..."
docker compose up --build -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Frontend:  http://localhost:3000"
echo "🔧 Backend:   http://localhost:8000"
echo "📖 API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "  docker compose logs -f        # Follow logs"
echo "  docker compose down           # Stop all services"
echo "  docker compose up -d          # Start in background"
