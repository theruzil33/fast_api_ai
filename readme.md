# FastAPI AI

## Структура репозитория

```
fast_api_ai/
├── backend/          # FastAPI-приложение (см. backend/readme.md)
└── docker-compose.yml
```

## Быстрый старт через Docker

```bash
cp .env.example .env
docker compose up --build
```

PostgreSQL поднимается автоматически. Приложение стартует после того, как БД будет готова.

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Остановить:
```bash
docker compose down
```

Остановить и удалить данные БД:
```bash
docker compose down -v
```
