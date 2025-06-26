# Используем официальный образ Python
FROM python:3.11

# 1. Устанавливаем ВСЕ необходимые зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновляем pip (это важно!)
RUN pip install --upgrade pip setuptools wheel

# 3. Создаем и переходим в рабочую директорию
WORKDIR /app

# 4. Сначала копируем только requirements.txt
COPY requirements.txt .

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальные файлы проекта
COPY . .

# 7. Команда для запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]