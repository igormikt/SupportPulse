# 1. Берем готовый образ Python (маленький и быстрый)
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь код проекта в контейнер
COPY . .

# 5. Открываем порт (внутри контейнера порт всегда 8000)
EXPOSE 8000

# 6. Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]