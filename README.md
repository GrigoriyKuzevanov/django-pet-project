# Django blog

[Описание проекта](./description.md)

## Русский

## Используемые технологии
- Django 4
- Postgresql
- Redis
- Celery

## Конфигурация
Используйте docker-compose для запуска:
- `docker-compose-local.yml` - файл для локального запуска
- `docker-compose-master.yml` - файо лоя щапуска на сервере
Перед запуском вам следует создать файл `.env` в корневой директории проекта и установить следующие переменные в нем:

```
ENV=.env

# Postgres
NAME_DB=
USER_DB=
PASSWORD_DB=
HOST_DB=
PORT_DB=

# Project settings
SECRET_KEY=

# Mail
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_USE_SSL=
EMAIL_PORT=

# Redis
REDIS_URL=redis://redis:6379/1

# Celery
CELERY_BROKER_URL=redis://127.0.0.1:6380/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6380/0
```


## Запуск


Старт на локальной машине:
```
docker-compose -f docker-compose-local.yml up --build
```
Старт на сервере
```
docker-compose -f docker-compose-master.yml up --build -d
```
Запустите оболочку внутри докер-контейнера приложения:
```
docker exec -it <APP_CONTAINER_ID> sh
```
Создайте суперюзера внуртри контейнера:
```
python3 manage.py createsuperuser
```

# English

## Technologies
- Django 4
- Postgresql
- Redis
- Celery

## Configuration
Use docker-compose to run project:
- `docker-compose-local.yml` - file for local run
- `docker-compose-master.yml` - file for production run

Before run the project you should add an `.env` file in the project root directory and set next variables in it:
```
ENV=.env

# Postgres
NAME_DB=
USER_DB=
PASSWORD_DB=
HOST_DB=
PORT_DB=

# Project settings
SECRET_KEY=

# Mail
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_USE_SSL=
EMAIL_PORT=

# Redis
REDIS_URL=redis://redis:6379/1

# Celery
CELERY_BROKER_URL=redis://127.0.0.1:6380/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6380/0
```


## Run project


Start docker local:
```
docker-compose -f docker-compose-local.yml up --build
```
Start docker in production
```
docker-compose -f docker-compose-master.yml up --build -d
```
Launch shell inside the app docker container:
```
docker exec -it <APP_CONTAINER_ID> sh
```
Create superuser for django app inside the container:
```
python3 manage.py createsuperuser
```
