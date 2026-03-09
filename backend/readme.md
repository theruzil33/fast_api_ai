# FastAPI AI

Базовый скелет FastAPI-приложения, готовый к расширению.

## Быстрый старт

### Локально

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Запустить тесты

```bash
.venv/bin/pytest tests/ -v
```

Запустить конкретный файл:
```bash
.venv/bin/pytest tests/test_my_feature.py -v
```

---

## Структура проекта

```
backend/
├── app/
│   ├── main.py                          # Создание экземпляра FastAPI, подключение роутеров
│   ├── core/
│   │   ├── config.py                    # Настройки приложения (ENV-переменные через pydantic-settings)
│   │   └── database.py                  # Подключение к БД (SQLAlchemy async engine)
│   ├── api/
│   │   └── v1/
│   │       ├── router.py                # Главный роутер v1 — сюда подключаются все эндпоинты
│   │       └── endpoints/
│   │           ├── health.py            # GET /api/v1/health/hello
│   │           └── projects.py          # CRUD /api/v1/projects
│   ├── models/
│   │   └── project.py                   # SQLAlchemy-модель Project
│   ├── schemas/
│   │   └── project.py                   # Pydantic-схемы для Project
│   └── services/
│       └── project_service.py           # Бизнес-логика для Project
├── tests/
│   ├── endpoints/
│   │   ├── test_health.py               # Тесты для /api/v1/health
│   │   └── test_projects.py             # Тесты для /api/v1/projects
│   └── services/
│       └── test_project_service.py      # Тесты для project_service
├── Dockerfile                           # Образ для запуска приложения
├── .env.example                         # Пример переменных окружения
├── pytest.ini                           # Конфигурация pytest
└── requirements.txt                     # Зависимости
```

---

### Добавить зависимость
```bash
pip install some-package
pip freeze | grep some-package >> requirements.txt
```

---

## Переменные окружения

| Переменная          | По умолчанию                                              | Описание                          |
|---------------------|-----------------------------------------------------------|-----------------------------------|
| `APP_NAME`          | `FastAPI AI`                                              | Название приложения               |
| `APP_VERSION`       | `0.1.0`                                                   | Версия приложения                 |
| `DEBUG`             | `false`                                                   | Режим отладки                     |
| `DATABASE_URL`      | `postgresql+asyncpg://user:password@localhost:5432/dbname`| URL подключения к БД              |
| `POSTGRES_USER`     | `user`                                                    | Пользователь PostgreSQL (Docker)  |
| `POSTGRES_PASSWORD` | `password`                                                | Пароль PostgreSQL (Docker)        |
| `POSTGRES_DB`       | `dbname`                                                  | Имя базы данных (Docker)          |
