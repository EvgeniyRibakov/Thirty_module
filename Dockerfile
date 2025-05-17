# Используем легковесный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем pip до последней версии
RUN pip install --upgrade pip

# Копируем файлы зависимостей для кэширования слоев
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main

# Копируем весь проект
COPY . .

# Проверяем наличие manage.py (для отладки)
RUN ls -la /app/myproject/manage.py || echo "manage.py not found"

# Команда по умолчанию для запуска Django
CMD ["python", "myproject/manage.py", "runserver", "0.0.0.0:8000"]