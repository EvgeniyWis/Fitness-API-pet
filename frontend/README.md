# Fitness Tracker Frontend

Фронтенд приложение для трекинга тренировок на Next.js.

## Технологии

- **Next.js 16** - React фреймворк с App Router
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **React 19** - UI библиотека

## Установка

```bash
npm install
```

## Запуск

```bash
npm run dev
```

Приложение будет доступно по адресу: `http://localhost:3000`

## Сборка

```bash
npm run build
npm start
```

## Структура проекта

```
frontend/
├── app/              # App Router (Next.js 13+)
│   ├── layout.tsx   # Корневой layout
│   ├── page.tsx     # Главная страница
│   └── globals.css  # Глобальные стили
├── public/          # Статические файлы
└── package.json
```

## Переменные окружения

Создайте файл `.env.local` в корне проекта:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```
