#!/bin/bash

# Remove virtual environment
rm -rf venv/

# Remove pip cache
pip cache purge

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} +

# Remove .pyc files
find . -type f -name "*.pyc" -delete 