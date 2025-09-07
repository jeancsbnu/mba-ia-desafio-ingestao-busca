#!/bin/bash
# Simple PDF ingestion script for easy use
# Usage: ./ingest.sh document.pdf

# Check if file is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a PDF file"
    echo "Usage: ./ingest.sh document.pdf"
    exit 1
fi

# Check if file exists
if [ ! -f "$1" ]; then
    echo "Error: File '$1' not found"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and run ingestion
echo "Processing PDF: $1"
echo "Please wait, this may take a few minutes..."

source venv/bin/activate
export PYTHONPATH=$(pwd)
python src/ingest.py "$1"

if [ $? -eq 0 ]; then
    echo "PDF processed successfully!"
    echo "Now you can search the document using: ./search.sh"
else
    echo "Error processing PDF. Please check the file and try again."
    exit 1
fi
