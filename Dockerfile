FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Устанавливаем Python-зависимости (включая Pillow)
RUN pip install --no-cache-dir -r requirements.txt pillow && \
    python manage.py migrate --noinput

# Очищаем build-зависимости (опционально)
RUN apt-get purge -y --auto-remove gcc python3-dev libffi-dev

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]