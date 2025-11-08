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
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd fastapi/Python-test

# 2. Создайте и активируйте виртуальное окружение (опционально)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Установите зависимости
 pip install -r requirements.txt

# 4. Запустите сервер разработки
uvicorn main:app --reload --port 8165
```

После запуска приложение будет доступно по адресу [http://localhost:8165](http://localhost:8165).

## Переменные окружения
| Переменная    | Назначение                            | Значение по умолчанию          |
|---------------|---------------------------------------|--------------------------------|
| `JWT_SECRET`  | Секрет для подписи JWT                | `change-me-in-production`      |
| `PORT`        | Порт для запуска (используется в примерах uvicorn) | `8165` |

Создайте файл `.env`, чтобы переопределить значения (опционально):
```
JWT_SECRET=super-secret-value
```

## Работа с API

1. **Логин и получение токена**
    ```bash
    curl -X POST http://localhost:8165/login ^
         -H "Content-Type: application/json" ^
         -d "{\"username\": \"admin\", \"password\": \"secret\"}"
    ```

    В ответе придёт `access_token`, `token_type` и `expires_in` (TTL в секундах).

2. **Доступ к защищённым маршрутам**
    ```bash
    TOKEN=<полученный токен>

    # Профиль пользователя и список фильмов
    curl http://localhost:8165/user ^
         -H "Authorization: Bearer %TOKEN%"

    # Добавление фильма (пример с curl и формой)
    curl -X POST http://localhost:8165/add_film ^
         -H "Authorization: Bearer %TOKEN%" ^
         -F "name=Новый фильм" ^
         -F "director=Режиссёр" ^
         -F "cost=1000000" ^
         -F "watched=true"
    ```

    Для доступа к HTML-форме `/add_film` авторизуйтесь в браузере, установив заголовок `Authorization` (см. [документацию FastAPI о Swagger UI](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/)).

## Тестовые данные
- Пользователь: `admin` / `secret`
- Фильмы: топ-10 в `app/data.py`