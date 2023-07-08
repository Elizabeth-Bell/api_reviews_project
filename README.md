# api_yamdb
api_yamdb, сервис, посвященный оценке произведений.
Вы можете добавить произведение, оставить свой отзыв, поставить оценку, прокомментировать чужие отзывы.

Как запустить проект:

Клонировать к себе репозиторий:

git clone https://github.com/Elizabeth-Bell/api_yamdb/

Cоздать и активировать виртуальное окружение:

python3 -m venv env source env/bin/activate Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip pip install -r requirements.txt Выполнить миграции:

python3 manage.py migrate Запустить проект:

python3 manage.py runserver

Для наполнения базы данных используйте команду:

python3 manage.py filling_database

Для запуска сервера выполните команду:

python3 manage.py runserver

Для просмотра документации при запущеном сервере перейдите по следующему адресу:

127.0.0.1:8000/redoc/

Над проектом работали:
Елизавета Беляева
Евгений Киричек
Вадим Агафонов
