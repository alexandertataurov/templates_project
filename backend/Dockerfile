FROM python:3.11-slim

# Install dependencies and LibreOffice
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice libreoffice-writer xvfb gcc libpq-dev default-jre \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

ENV UNO_PATH="/usr/lib/libreoffice/program"
ENV PATH="$UNO_PATH:$PATH"

WORKDIR /app

# Copy requirements and install dependencies as root
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application and set ownership
COPY --chown=appuser:appuser . .

# Make start.sh executable
RUN chmod +x start.sh

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["./start.sh"]