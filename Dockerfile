# Используем официальный образ Python
FROM python:3.11-slim

# 1. Устанавливаем системные зависимости ДО установки пакетов
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновляем pip
RUN pip install --upgrade pip

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Сначала копируем только requirements.txt
COPY requirements.txt .

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальные файлы
COPY . .


# 7. Команда для запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]