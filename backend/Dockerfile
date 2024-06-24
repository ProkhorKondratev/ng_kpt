# Используем базовый образ Python
FROM python:3.12.2-slim-bookworm

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем Redis
RUN apt-get update && apt-get install -y redis-server

# Устанавливаем supervisor
RUN apt-get install -y supervisor

# Обновляем pip и устанавливаем зависимости Python
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем настройки supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY supervisord.conf /etc/supervisord.conf

# Копируем исходный код приложения
COPY . .

# Запускаем supervisor
CMD ["/usr/bin/supervisord"]
