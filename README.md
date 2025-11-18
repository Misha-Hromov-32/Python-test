# FastAPI BGITU

Приложение на FastAPI для управления списком фильмов
Продемонстрирована модульная архитектура, SQLite, загрузка файлов, защита маршрутов и работа с PyJWT.

## Возможности
- Авторизация по JWT (`/login`) с хранением пользователей в SQLite и хэшированием паролей.
- Защищённые маршруты `/user` и `/add_film` (GET/POST) с проверкой заголовка `Authorization: Bearer <token>`.
- Список фильмов, просмотр карточки фильма и HTML-форма добавления нового фильма.
- Загрузка постеров и файлов описания с сохранением в `static/posters` и `uploads/descriptions`.

## Структура проекта
```
Python-test/
├── app/
│   ├── core/config.py       # настройки и создание директорий
│   ├── data.py              # тестовые пользователи и фильмы
│   ├── database.py          # работа с SQLite
│   ├── dependencies.py      # общие зависимости (аутентификация)
│   ├── models.py            # Pydantic-модели
│   ├── routers/
│   │   ├── auth.py          # /login, /user
│   │   └── movies.py        # /movies, /movietop, /add_film
│   ├── schemas/             # pydantic-схемы запросов/ответов
│   └── security.py          # PyJWT, хэширование, журнал обращений
├── main.py                  # точка входа (uvicorn)
├── requirements.txt         # зависимости проекта
├── templates/               # Jinja2-шаблоны
└── static/, uploads/        # статические файлы и загрузки
```

## Старт
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/Misha-Hromov-32/Python-test.git
cd Python-test

# 2. Создайте и активируйте виртуальное окружение (опционально)
python -m venv .env
.env\Scripts\activate  # Windows
# source .env/bin/activate  # macOS/Linux

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите сервер разработки
python main.py
```

После запуска приложение будет доступно по адресу [http://localhost:8165](http://localhost:8165).

## Переменные окружения
| Переменная    | Назначение                            | Значение по умолчанию          |
|---------------|---------------------------------------|--------------------------------|
| `JWT_SECRET`  | Секрет для подписи JWT                | `change-me-in-production`      |
| `PORT`        | Порт для запуска (используется в примерах uvicorn) | `8165` |

## Работа с API

1. **Логин и получение токена**
    ```bash
    curl -X POST http://localhost:8165/login ^
         -H "Content-Type: application/json" ^
         -d "{\"username\": \"admin\", \"password\": \"secret\"}"
    ```

    В ответе придёт `access_token`, `token_type` и `expires_in` (TTL в секундах).

## Тестовые данные
- Пользователь: `admin` / `secret`
- Фильмы: топ-10 в `app/data.py`