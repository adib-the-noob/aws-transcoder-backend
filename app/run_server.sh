#!/bin/bash

# Determine the operating system and set the requirements file
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    REQ_FILE="requirements.txt"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32" ]]; then
    REQ_FILE="requirements_win.txt"
else
    echo "Unsupported operating system"
    exit 1
fi

# Check if env folder exists, if not create it and install requirements
if [ ! -d "env" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv env
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Make sure python3 and venv are installed."
        exit 1
    fi
    
    # Activate the new environment
    source env/bin/activate || source env/Scripts/activate
    
    echo "Installing requirements from $REQ_FILE..."
    pip install -r $REQ_FILE
    if [ $? -ne 0 ]; then
        echo "Failed to install requirements. Please check your $REQ_FILE file."
        exit 1
    fi
else
    # Activate the existing environment
    source env/bin/activate || source env/Scripts/activate
fi

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "Failed to activate the virtual environment."
    exit 1
fi

# Run the server
exec uvicorn app:app --host 0.0.0.0 --port 8000