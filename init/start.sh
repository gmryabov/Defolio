#!/bin/bash

set -euo pipefail

# Переход в корень проекта (один уровень выше папки init)
cd "$(dirname "$0")/.."

echo "Рабочая директория: $(pwd)"

# Создаём сеть shared_network, если её ещё нет
if ! docker network inspect shared_network >/dev/null 2>&1; then
  echo "Создаём сеть shared_network..."
  docker network create shared_network
else
  echo "Сеть shared_network уже существует"
fi

# Запускаем все compose-файлы одной командой
echo "Запускаем docker-compose..."

docker compose \
  -f postgres/docker-compose.yml \
  -f redis/docker-compose.yml \
  -f nginx_manager/docker-compose.yml \
  -f backend/docker-compose.yml \
  -f celery/docker-compose.yml \
  up -d --build

echo "Все сервисы запущены."
