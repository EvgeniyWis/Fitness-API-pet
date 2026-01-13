# Fitness Tracker - Full Stack Application

Полнофункциональное приложение для трекинга тренировок в тренажерном зале и волейболе.

## 📁 Структура проекта

```
fitness-api-pet/
├── backend/          # FastAPI бэкенд
│   ├── app/         # Основной код приложения
│   ├── alembic/     # Миграции базы данных
│   ├── pyproject.toml
│   └── README.md    # Документация бэкенда
│
├── frontend/        # React фронтенд
│   ├── src/        # Исходный код
│   ├── package.json
│   └── README.md   # Документация фронтенда
│
└── ARCHITECTURE.md # Архитектура проекта
```

## 🚀 Быстрый старт

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Backend будет доступен на `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на `http://localhost:3000` (Next.js по умолчанию использует порт 3000)

## 📚 Документация

- **Backend**: См. [backend/README.md](backend/README.md)
- **Frontend**: См. [frontend/README.md](frontend/README.md)
- **Архитектура**: См. [ARCHITECTURE.md](ARCHITECTURE.md)

## 🛠 Технологии

### Backend
- FastAPI
- SQLModel/SQLAlchemy
- Alembic
- Redis
- JWT аутентификация

### Frontend
- Next.js 16
- TypeScript
- Tailwind CSS
- React 19

## 📝 Лицензия

MIT
