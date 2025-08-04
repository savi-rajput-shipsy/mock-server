#!/bin/bash

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Warning: Virtual environment not found at .venv/bin/activate"
    echo "Continuing without virtual environment..."
fi

# Start the server
python3 -m uvicorn mock_server:app --reload --port 8000 