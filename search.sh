#!/bin/bash
# Simple document search script for easy use
# Usage: ./search.sh "your question here"

# Check if question is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a question"
    echo "Usage: ./search.sh \"What companies are mentioned?\""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and run search
echo "Searching for: $1"
echo "Please wait..."

source venv/bin/activate
export PYTHONPATH=$(pwd)
python src/search.py "$1"

if [ $? -eq 0 ]; then
    echo ""
    echo "Search completed!"
else
    echo "Error during search. Please try again."
    exit 1
fi
