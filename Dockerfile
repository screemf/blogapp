# Используем официальный образ Python
FROM python:3.9-slim  # или python:3.9 для полной версии

# 1. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Копируем остальные файлы проекта
COPY . .

# 5. Команда для запуска (замените на свою)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]