# Используем официальный образ Python с конкретной версией
FROM python:3.11.6-bookworm

# 1. Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновляем pip и setuptools
RUN pip install --upgrade pip setuptools wheel

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Копируем requirements.txt отдельно для кэширования
COPY requirements.txt .

# 5. Устанавливаем зависимости (сначала cffi отдельно)
RUN pip install --no-cache-dir cffi==1.16.0 && \
    pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальные файлы проекта
COPY . .

# 7. Команда для запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]