#!/bin/bash

# Attempt to activate the virtual environment
if [ -f "env/bin/activate" ]; then
    source env/bin/activate
elif [ -f "env/Scripts/activate" ]; then
    source env/Scripts/activate
else
    echo "Virtual environment not found. Make sure it's created and in the correct location."
    exit 1
fi

# Run the server
exec uvicorn app:app --host 0.0.0.0 --port 8000