# Блог на Django
---

## УСТАНОВКА И ЗАПУСК

**Создать виртуальное окружение**
```
python3 -m venv env
```

**Установить зависимости**
```
pip install -r requirements.txt
```

**Создать файл .env, в котором создать переменные для подключения к базе данных**
```
NAME_DB=<your_db_name>
USER_DB=<your_user_name>
PASSWORD_DB=s<your_password>
HOST_DB=<your_host>
PORT_DB=<your_port>
```

**Создать миграции и таблицы в БД (for linux)**
```
cd articles
python manage.py makemigrations
python manage.py migrate
```

**Запуск**
```
python manage.py runserver
```

**Начальная страница доступна по адресу**
```
127.0.0.1:8000/blog/
```

---

## О ПРОЕКТЕ

Учебный проект - Блог с использованием фреймворка Django.
Реализована система авторизации и аутентификации пользователей, добавление записей, комментарии, система тэгов, отображение записей по
категориям.
