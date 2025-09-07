#!/bin/bash
# Simple document list script
# Usage: ./list.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup first."
    exit 1
fi

echo "Listing processed documents..."
echo ""

source venv/bin/activate
export PYTHONPATH=$(pwd)
python -m src.presentation.cli.interface list-documents

if [ $? -eq 0 ]; then
    echo ""
    echo "Document list retrieved successfully!"
else
    echo "Error retrieving document list."
    exit 1
fi
