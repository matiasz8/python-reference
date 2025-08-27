#!/bin/bash

# Start server script for Greenhouse API Proxy
# Usage: ./scripts/start_server.sh [test|prod]

set -e

# Default to test mode
MODE=${1:-test}

echo "🚀 Starting Greenhouse API Proxy Server"
echo "Mode: $MODE"
echo "========================================"

if [ "$MODE" = "test" ]; then
    echo "📝 Starting in TEST MODE with mock data"
    echo "Dashboard will show sample data for testing"
    echo ""
    echo "Dashboard URL: http://localhost:8000/dashboard/"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""

    TEAMTAILOR_TEST_MODE=true pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

elif [ "$MODE" = "prod" ]; then
    echo "🌐 Starting in PRODUCTION MODE"
    echo "Will connect to real TeamTailor API"
    echo ""
    echo "Make sure you have valid TeamTailor credentials configured"
    echo "Dashboard URL: http://localhost:8000/dashboard/"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""

    pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

else
    echo "❌ Invalid mode. Use 'test' or 'prod'"
    echo "Usage: ./scripts/start_server.sh [test|prod]"
    exit 1
fi
