# Frontend

React + TypeScript + Vite приложение.

## Запуск и сборка

### Установка зависимостей
```bash
npm install
```

### Запуск в режиме разработки
```bash
npm run dev
```
Приложение будет доступно на `http://localhost:5173`

### Сборка для продакшена
```bash
npm run build
```
Собранные файлы появятся в папке `dist/`

### Предпросмотр собранного приложения
```bash
npm run preview
```

### Линтинг
```bash
npm run lint
```

### Сборка и запуск в Docker
```bash
docker build -t frontend .
docker run -p 3000:80 frontend
```
Приложение будет доступно на `http://localhost:3000`

### Запуск всего стека (frontend + backend + БД) через Docker Compose

В корне проекта находится `docker-compose.full.yml`, который поднимает все сервисы сразу:

```bash
# из корня проекта
docker compose -f docker-compose.full.yml up --build
```

| Сервис   | Адрес                   |
|----------|-------------------------|
| Frontend | http://localhost:3000   |
| Backend  | http://localhost:8000   |

Остановка:
```bash
docker compose -f docker-compose.full.yml down
```

---

## Структура проекта

```
frontend/
├── public/                  # Статические файлы (отдаются как есть)
│   └── vite.svg
├── src/
│   ├── main.tsx             # Точка входа — монтирует React-приложение
│   ├── App.tsx              # Корневой компонент, роутинг
│   ├── types.ts             # Общие TypeScript-типы
│   ├── assets/              # Изображения и прочие ресурсы
│   └── pages/               # Страницы приложения
│       └── projects/        # Страница управления проектами
│           ├── index.tsx            # Главный компонент страницы
│           ├── index.styles.ts      # Стили (styled-components)
│           ├── ProjectForm.tsx      # Форма создания/редактирования проекта
│           ├── ProjectsTable.tsx    # Таблица со списком проектов
│           ├── ProjectsFilter.tsx   # Фильтрация проектов
│           └── DeleteButton.tsx     # Кнопка удаления проекта
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### Стек
- **React 19** — UI-библиотека
- **TypeScript** — типизация
- **Vite** — сборщик и dev-сервер
- **styled-components** — CSS-in-JS стили
