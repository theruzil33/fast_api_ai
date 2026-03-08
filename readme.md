# FastAPI AI

Базовый скелет FastAPI-приложения, готовый к расширению.

## Быстрый старт

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Структура проекта

```
fast_api_ai/
├── app/
│   ├── main.py                     # Создание экземпляра FastAPI, подключение роутеров
│   ├── core/
│   │   └── config.py               # Настройки приложения (ENV-переменные через pydantic-settings)
│   ├── api/
│   │   └── v1/
│   │       ├── router.py           # Главный роутер v1 — сюда подключаются все эндпоинты
│   │       └── endpoints/
│   │           └── health.py       # Пример эндпоинта: GET /api/v1/health/hello
│   └── schemas/                    # Pydantic-схемы для валидации запросов и ответов
├── tests/
│   └── test_health.py              # Тесты для /api/v1/health/hello
├── .env.example                    # Пример переменных окружения
└── requirements.txt                # Зависимости
```

---

## Где что менять

### Добавить новый эндпоинт
1. Создать файл `app/api/v1/endpoints/my_feature.py` с `APIRouter`
2. Зарегистрировать роутер в `app/api/v1/router.py`:
   ```python
   from app.api.v1.endpoints import my_feature
   api_router.include_router(my_feature.router, prefix="/my-feature", tags=["my-feature"])
   ```

### Добавить настройку (ENV-переменную)
Открыть `app/core/config.py`, добавить поле в класс `Settings`:
```python
DATABASE_URL: str = "sqlite:///./db.sqlite3"
```
Затем добавить переменную в `.env`.

### Добавить Pydantic-схему
Создать файл в `app/schemas/`, например `app/schemas/user.py`:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
```

### Добавить новую версию API (v2)
Скопировать структуру `app/api/v1/` в `app/api/v2/` и подключить новый роутер в `app/main.py`:
```python
app.include_router(api_router_v2, prefix="/api/v2")
```

### Добавить тест для нового эндпоинта
Создать файл `tests/test_my_feature.py`:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_my_endpoint():
    response = client.get("/api/v1/my-feature/something")
    assert response.status_code == 200
    assert response.json() == {"key": "value"}
```

Запустить тесты:
```bash
.venv/bin/pytest tests/ -v
```

Запустить конкретный файл:
```bash
.venv/bin/pytest tests/test_my_feature.py -v
```

---

### Добавить зависимость
```bash
pip install some-package
pip freeze | grep some-package >> requirements.txt
```

---

## Переменные окружения

| Переменная    | По умолчанию | Описание                    |
|---------------|--------------|-----------------------------|
| `APP_NAME`    | `FastAPI AI` | Название приложения         |
| `APP_VERSION` | `0.1.0`      | Версия приложения           |
| `DEBUG`       | `false`      | Режим отладки               |
