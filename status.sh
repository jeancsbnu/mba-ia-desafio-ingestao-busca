#!/bin/bash
# Simple system status check script
# Usage: ./status.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup first."
    exit 1
fi

echo "Checking system status..."
echo ""

source venv/bin/activate
export PYTHONPATH=$(pwd)
python -m src.presentation.cli.interface status

if [ $? -eq 0 ]; then
    echo ""
    echo "System is ready to use!"
    echo "Available commands:"
    echo "   ./ingest.sh document.pdf  - Process a PDF file"
    echo "   ./search.sh \"question\"    - Search documents"
    echo "   ./chat.sh                 - Interactive chat mode"
    echo "   ./list.sh                 - List processed documents"
else
    echo "System has issues. Please check the configuration."
    exit 1
fi
