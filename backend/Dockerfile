FROM python:3.11-slim

# Устанавливаем зависимости и LibreOffice
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice libreoffice-writer xvfb gcc libpq-dev default-jre \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


ENV UNO_PATH="/usr/lib/libreoffice/program"
ENV PATH="$UNO_PATH:$PATH"

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "if ! pgrep Xvfb; then Xvfb :1 -screen 0 1024x768x16 & fi && \
    soffice --headless --accept='socket,host=localhost,port=8100;urp;' --nologo --nodefault --nofirststartwizard --norestore & \
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]

