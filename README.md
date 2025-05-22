# YaCut - Сервис укорочения ссылок

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4%2B-red)](https://www.sqlalchemy.org/)

Сервис для преобразования длинных URL в короткие удобные ссылки.

## Возможности

- Генерация коротких ссылок (6 случайных символов)
- Возможность указать свой вариант короткой ссылки
- Переадресация по коротким ссылкам
- REST API для интеграции с другими сервисами
- Валидация вводимых данных

## Технологии

- Python 3.7+
- Flask 2.0+
- SQLAlchemy 1.4+
- Bootstrap 5 (для фронтенда)
- WTForms (для валидации)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Viocid/yacut.git
   cd yacut
Создайте и активируйте виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
Установите зависимости:

bash
pip install -r requirements.txt
Настройте переменные окружения:

bash
export FLASK_APP=yacut
export FLASK_ENV=development
export DATABASE_URI=sqlite:///db.sqlite3
Инициализируйте базу данных:

bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Запуск
bash
flask run
Сервис будет доступен по адресу: http://localhost:5000

API
Сервис предоставляет REST API для работы с короткими ссылками:

Создание короткой ссылки
POST /api/id/
Пример запроса:

json
{
  "url": "https://example.com",
  "custom_id": "example"
}
Пример ответа:

json
{
  "url": "https://example.com",
  "short_link": "http://localhost/example"
}
Получение оригинальной ссылки
GET /api/id/<short_id>/
Пример ответа:

json
{
  "url": "https://example.com"
}
Структура проекта
yacut/
├── yacut/               # Основной пакет приложения
│   ├── __init__.py      # Инициализация приложения
│   ├── models.py        # Модели базы данных
│   ├── forms.py         # Формы для ввода данных
│   ├── views.py         # Основные view-функции
│   ├── api_views.py     # API endpoints
│   ├── error_handlers.py # Обработчики ошибок
│   ├── utils.py         # Вспомогательные функции
│   └── templates/       # Шаблоны
├── tests/               # Тесты
├── config.py            # Конфигурация
└── requirements.txt     # Зависимости