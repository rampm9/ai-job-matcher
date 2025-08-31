#!/bin/bash

# JobMatch Checker - Quick Start Script
echo "🚀 Starting JobMatch Checker..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for API key
if [ -f ".env" ] && grep -q "OPENAI_API_KEY" .env; then
    echo "🔑 OpenAI API key found in .env file"
elif [ -n "$OPENAI_API_KEY" ]; then
    echo "🔑 OpenAI API key found in environment"
else
    echo "⚠️  No OpenAI API key configured - running in fallback mode"
    echo "   To add API key: echo 'OPENAI_API_KEY=sk-your-key' > .env"
fi

# Start the application
echo "🌐 Starting JobMatch Checker on http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "💚 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn src.app:app --reload --port 8000
