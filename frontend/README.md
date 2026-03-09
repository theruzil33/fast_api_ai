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
