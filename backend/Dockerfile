# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apt-get update && apt-get install -y cron && apt-get install nano && apt-get clean

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Выполняем миграции и запускаем приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]