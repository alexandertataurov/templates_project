# Используем официальный образ Python 3.11
FROM python:3.11

# Устанавливаем зависимости для работы LibreOffice и unoconv
RUN apt-get update && apt-get install -y \
    libreoffice \
    unoconv \
    python3-uno \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем переменные окружения для работы unoconv
ENV UNO_PATH="/usr/lib/libreoffice/program"
ENV PYTHONPATH="/usr/lib/python3/dist-packages"
ENV PATH="$UNO_PATH:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запускаем FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
