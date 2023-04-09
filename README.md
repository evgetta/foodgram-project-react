![example workflow](https://github.com/evgetta/foodgram-project-react/actions/workflows/foodgram_main.yml/badge.svg)

# Продуктовый помощник

Это онлайн-сервис, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на других авторов, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Используемые технологии:

Python 3.7 
Django 2.2.16 
Docker 23.0.0 
Docker-compose 1.29.2

## Варианты запуска

### Запуск проекта в dev-режиме без Docker контейнеров, перейти в корневую папку и выполнить:
```
python -m venv venv
source venv/Scripts/activate (Windows)
source venv/bin/activate (macOS или Linux)
cd backend/
python -m pip install --upgrade pip
pip install -r requirements.txt
```
#### Создаем env-файл, используемая БД - SQLite:
```
echo '''SECRET_KEY=some_secret_key
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
''' > .env
```
#### Запуск проекта
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
http://localhost/

### Запуск проекта в Docker контейнерах:

#### Перейти в папку infra/ и cоздать env-файл, используемая БД - PostgreSQL:
```
echo '''SECRET_KEY=some_secret_key
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db 
DB_PORT=5432
''' > .env
```
#### Сборка и запуск контейнеров
```
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py load_tags
docker-compose exec backend python manage.py load_ingredients
```

### Автор
Заозерских Евгений
