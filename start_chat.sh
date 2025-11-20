#!/bin/bash

# Simple startup script for Tinker Chat Interface

echo "╔════════════════════════════════════════╗"
echo "║    🤖 Tinker Chat Interface Setup    ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if TINKER_API_KEY is set
if [ -z "$TINKER_API_KEY" ]; then
    echo "❌ ERROR: TINKER_API_KEY not set!"
    echo ""
    echo "Please set your API key:"
    echo "  export TINKER_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key from:"
    echo "  https://tinker-console.thinkingmachines.ai"
    echo ""
    exit 1
fi

echo "✅ TINKER_API_KEY is set"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "🚀 Starting Tinker Chat Interface..."
echo ""
echo "The app will open at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "════════════════════════════════════════"
echo ""

# Run the app
python3 app.py

