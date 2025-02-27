#!/bin/bash
set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Start Xvfb
log "Starting Xvfb..."
Xvfb :1 -screen 0 1024x768x16 &
export DISPLAY=:1

# Wait for Xvfb to be ready
sleep 2

# Start LibreOffice in headless mode
log "Starting LibreOffice in headless mode..."
soffice --headless --accept='socket,host=localhost,port=8100;urp;' --nologo --nodefault --nofirststartwizard --norestore &

# Wait for LibreOffice to be ready
sleep 2

# Start uvicorn
log "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload