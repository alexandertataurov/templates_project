#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core requirements
pip install -r requirements.txt

# Install development requirements if in dev mode
if [ "$1" = "dev" ]; then
    pip install -r requirements.dev.txt
fi

# Generate requirements.txt from current environment
pip freeze > requirements.txt 