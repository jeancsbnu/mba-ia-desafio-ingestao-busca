#!/bin/bash
# Simple interactive chat script for easy use
# Usage: ./chat.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup first."
    exit 1
fi

echo "Starting interactive chat mode..."
echo "Type 'help' for available commands"
echo "Type 'quit', 'exit', or 'q' to exit"
echo "=================================================="

# Activate virtual environment and run chat
source venv/bin/activate
export PYTHONPATH=$(pwd)
python src/chat.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Chat session ended."
else
    echo "Error during chat session. Please try again."
    exit 1
fi
