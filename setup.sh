#!/bin/bash
# Simple setup script for easy installation
# Usage: ./setup.sh

echo "Setting up PDF Search System..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.11+ first."
    echo "   Download from: https://python.org"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    echo "   Download from: https://docker.com"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "Prerequisites check passed!"
echo ""

# Create virtual environment
echo "Creating Python environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error creating virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

# Configure Google Gemini as default
echo "Configuring AI service..."
python src/setup.py google
if [ $? -ne 0 ]; then
    echo "Error configuring AI service"
    exit 1
fi

# Start database
echo "Starting database..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Error starting database"
    exit 1
fi

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Initialize database
echo "Initializing database..."
export PYTHONPATH=$(pwd)
python -m src.config.database
if [ $? -ne 0 ]; then
    echo "Error initializing database"
    exit 1
fi

# Make scripts executable
chmod +x *.sh

echo ""
echo "Setup completed successfully!"
echo ""
echo "Your PDF Search System is ready to use!"
echo ""
echo "Quick Start Guide:"
echo "   1. Process a PDF: ./ingest.sh document.pdf"
echo "   2. Search documents: ./search.sh \"What companies are mentioned?\""
echo "   3. Check status: ./status.sh"
echo "   4. List documents: ./list.sh"
echo ""
echo "For more help, see the README.md file"
