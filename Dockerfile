FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем проект
COPY . .

ENV PYTHONUNBUFFERED=1

# Для разработки мы запускаем runserver через docker-compose
