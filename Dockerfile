FROM python:3.11-slim

# Установка инструментов для диагностики
RUN apt-get update && apt-get install -y \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/logs

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]