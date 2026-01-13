# Архитектура проекта: Frontend + Backend

## Структура проекта

```
fitness-api-pet/
├── backend/           # FastAPI бэкенд
│   ├── app/          # Основной код приложения
│   │   ├── api/      # API роутеры
│   │   ├── core/     # Конфигурация и настройки
│   │   ├── models/   # SQLModel модели
│   │   ├── repositories/ # Repository Pattern
│   │   ├── services/ # Бизнес-логика
│   │   ├── security/ # Утилиты безопасности
│   │   └── main.py   # Точка входа
│   ├── alembic/      # Миграции базы данных
│   ├── pyproject.toml
│   └── README.md
│
└── frontend/         # Next.js фронтенд приложение
    ├── app/          # App Router (Next.js 13+)
    │   ├── layout.tsx # Корневой layout
    │   ├── page.tsx  # Страницы
    │   └── globals.css # Глобальные стили
    ├── public/       # Статические файлы
    ├── package.json
    └── next.config.ts
```

## Разделение ответственности

### Backend (FastAPI)

**Ответственность:**

- REST API эндпоинты
- Бизнес-логика и валидация данных
- Работа с базой данных
- Аутентификация и авторизация (JWT токены)
- Статистика и агрегация данных

**Технологии:**

- FastAPI
- SQLModel/SQLAlchemy
- Redis (для токенов)
- Alembic (миграции)

**API эндпоинты:**

- `POST /api/auth/register` - регистрация
- `POST /api/auth/login` - вход (устанавливает JWT в cookies)
- `POST /api/auth/logout` - выход
- `POST /api/auth/refresh` - обновление токена
- `GET /api/workouts` - список тренировок (с фильтрацией и пагинацией)
- `POST /api/workouts` - создание тренировки
- `GET /api/workouts/{id}` - получение тренировки
- `PUT /api/workouts/{id}` - обновление тренировки
- `DELETE /api/workouts/{id}` - удаление тренировки
- `GET /api/stats` - статистика (только для админов)

### Frontend (React + TypeScript)

**Ответственность:**

- Пользовательский интерфейс
- Взаимодействие с API через HTTP запросы
- Управление состоянием приложения
- Роутинг и навигация
- Обработка форм и валидация на клиенте

**Технологии:**

- React 18
- TypeScript
- Vite (сборщик)
- React Router (роутинг)
- Axios (HTTP клиент)

**Структура:**

- `src/api/` - API клиенты (auth, workouts, stats)
- `src/components/` - переиспользуемые компоненты
- `src/pages/` - страницы приложения
- `src/App.tsx` - главный компонент с роутингом

## Взаимодействие Frontend ↔ Backend

### Аутентификация

1. **Вход (Login):**

   - Frontend отправляет `POST /api/auth/login` с username и password
   - Backend проверяет credentials и устанавливает JWT токены в HTTP-only cookies
   - Backend возвращает токены в ответе (для удобства, но основное хранение в cookies)

2. **Автоматическая аутентификация:**

   - Все запросы к защищенным эндпоинтам автоматически включают cookies (благодаря `withCredentials: true` в axios)
   - Backend проверяет токен из cookies через middleware

3. **Обновление токена:**
   - Frontend может вызвать `POST /api/auth/refresh` для обновления access токена
   - Refresh токен также хранится в cookies

### CORS настройка

Backend настроен для работы с фронтендом:

- Разрешенные origins: `http://localhost:3000`, `http://localhost:5173`
- `allow_credentials: true` - для работы с cookies
- Разрешены все методы и заголовки

### API клиент

Базовый API клиент (`src/api/client.ts`):

- Настроен на `http://localhost:8000/api`
- `withCredentials: true` - автоматическая отправка cookies
- Интерцептор для обработки 401 ошибок (редирект на /login)

## Запуск проекта

### Backend

```bash
# В директории backend/
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Backend будет доступен на `http://localhost:8000`

### Frontend

```bash
# В директории frontend/
cd frontend
npm install
npm run dev
```

Frontend будет доступен на `http://localhost:3000`

## Переменные окружения

### Backend

Создайте `.env` файл в директории `backend/` (уже должен быть):

```
DATABASE_URL=sqlite:///./fitness.db
SECRET_KEY=your-secret-key
...
```

### Frontend

Создайте `.env.local` файл в `frontend/`:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## Разработка

### Рекомендуемый workflow

1. **Backend разработка:**

   - Изменения в API эндпоинтах
   - Тестирование через Swagger UI (`http://localhost:8000/docs`)
   - Миграции БД через Alembic

2. **Frontend разработка:**

   - Разработка компонентов и страниц в `app/`
   - Использование Server Components и Client Components
   - Hot reload через Next.js dev server

3. **Интеграция:**
   - Проверка работы CORS
   - Тестирование аутентификации
   - Проверка работы с cookies

## Следующие шаги для фронтенда

1. **Реализация страниц:**

   - `app/login/page.tsx` - форма входа
   - `app/register/page.tsx` - форма регистрации
   - `app/workouts/page.tsx` - список и CRUD операции для тренировок
   - `app/stats/page.tsx` - отображение статистики

2. **API клиент:**

   - Создать утилиты для работы с API в `lib/api/`
   - Настроить обработку cookies для JWT токенов
   - Реализовать interceptors для обработки ошибок

3. **Управление состоянием:**

   - Context API для хранения текущего пользователя
   - Или Zustand/Redux для более сложного состояния
   - Server Components для данных с сервера

4. **Защита роутов:**

   - Middleware для проверки аутентификации
   - Redirect на страницу входа при отсутствии токена

5. **Обработка ошибок:**

   - Error boundaries для Client Components
   - `error.tsx` файлы для обработки ошибок в роутах
   - Обработка ошибок API запросов

6. **UI/UX:**

   - Использовать Tailwind CSS для стилизации
   - Добавить библиотеку компонентов (shadcn/ui, или собственная)
   - Добавить loading states (loading.tsx)

7. **Валидация форм:**
   - React Hook Form
   - Валидация на клиенте перед отправкой
   - Server Actions для обработки форм
