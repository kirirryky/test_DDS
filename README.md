Money Moving - Веб-сервис для управления движением денежных средств (ДДС)

Функционал:
- Добавление транзакций
- Управление справочниками (типы, статусы, категории, подкатегории)
- Фильтрация и сортировка транзакций по дате, сумме, статусу, категории
- Редактирование и удаление записей
- Удобный интерфейс на Bootstrap 5

Технологии:
- Python 3.15
- Django 6.0.6
- Bootstrap 5.3.2
- SQLite (база данных)

Установка и запуск:
1. Клонируйте репозиторий

2. Создайте виртуальное окружение
Windows:
python -m venv venv
venv\Scripts\activate

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

3. Установите зависимости:
pip install -r requirements.txt

4. Примените миграции:
python manage.py migrate

5. Создайте суперпользователя:
python manage.py createsuperuser

6. Запустите сервер:
python manage.py runserver

7. Откройте сервис в браузере:
локалка:
http://127.0.0.1:8000/


