# Используем официальный образ Python с конкретной версией
FROM python:3.11-bookworm  # или python:3.11-slim для более легкого образа

# 1. Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновляем pip до последней версии
RUN pip install --upgrade pip

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Сначала копируем только requirements.txt для кэширования
COPY requirements.txt .

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальные файлы проекта
COPY . .

# 7. Команда для запуска (замените на свою)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]