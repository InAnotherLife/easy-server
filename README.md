# Приложение "Easy Server"

https://github.com/InAnotherLife/easy-server

https://t.me/JohnWooooo

[![Easy Server workflow](https://github.com/InAnotherLife/easy-server/actions/workflows/main.yml/badge.svg)](https://github.com/InAnotherLife/easy-server/actions/workflows/main.yml)

## О проекте
Программа представляет собой простое веб-приложение.\
Приложение разработано на языке Python версии 3.9 с использованием фреймворка Flask. Для работы с БД использовалось расширение Flask-SQLAlchemy. Для работы с токенами использовалось расширение Flask-JWT-Extended. Для хеширования и проверки паролей использовалась библиотека Werkzeug.\
Код программы находится в папке src.

## Стек
* Python 3.9
* Flask 3.0.3
* Flask-SQLAlchemy 3.1.1
* Flask-JWT-Extended 4.6.0
* Werkzeug 3.0.3

## Запуск приложения
В корне проекта создать файл .env. Пример заполнения файла:
```
JWT_SECRET_KEY='secret_key'
```

Необходимо создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Перейти в папку src и запустить приложение:
```
cd src
python server.py
```

## Работа с приложением
После запуска приложения доступны следующие эндпойты:

1. Регистрация нового пользователя
```
POST http://127.0.0.1:5000/register
```

2. Авторизация пользователя
```
POST http://127.0.0.1:5000/login
```

3. Получение всех пользователей
```
GET http://127.0.0.1:5000/users
```

4. Получение информации о конкретном пользователе по id
```
GET http://127.0.0.1:5000/users/{id}
```

5. Обновление информации о пользователе по id
```
PATCH http://127.0.0.1:5000/users/{id}
```

5. Удаление пользователя по id
```
DELETE http://127.0.0.1:5000/users/{id}
```