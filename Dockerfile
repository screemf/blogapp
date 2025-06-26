FROM python:3.11-slim

# Установка curl для healthcheck
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/healthcheck/ || exit 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]