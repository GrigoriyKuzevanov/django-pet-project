# Django blog
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
NAME_DB=a
USER_DB=a
PASSWORD_DB=
HOST_DB=
PORT_DB=

# Project settings
SECRET_KEY=
DEBUG=

# Mail
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_USE_SSL=
EMAIL_PORT=
```


## Run project


**Local**
```
docker-compose -f docker-compose-local.yml up --build
```

**Production**

Start docker:
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
