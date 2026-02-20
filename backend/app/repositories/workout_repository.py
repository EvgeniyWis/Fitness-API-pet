from datetime import date

from sqlalchemy.orm import Session

from app.models.workout import GymType, Workout
from app.utils.date_utils import convert_date_string
from app.utils.db_decorator import with_db_session


class WorkoutRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""

    def _filter_workouts(
        self,
        query,
        user_id: int = None,
        type: GymType | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        min_duration: int | None = None,
        max_duration: int | None = None,
        page: int = 1,
        size: int = 10,
    ):
        """
        Применяет фильтры к SQLAlchemy query объекту.

        Args:
            query: SQLAlchemy query объект
            user_id: ID пользователя
            type: Тип тренировки
            date_from: Начальная дата (включительно)
            date_to: Конечная дата (включительно)
            min_duration: Минимальная длительность
            max_duration: Максимальная длительность
            page: Номер страницы
            size: Количество элементов на странице

        Returns:
            Отфильтрованный query объект с примененной пагинацией
        """
        # Применяем фильтры на уровне SQL запроса
        if user_id is not None:
            query = query.filter(Workout.user_id == user_id)

        if type is not None:
            query = query.filter(Workout.type == type)

        if date_from is not None:
            query = query.filter(Workout.planned_date >= date_from)

        if date_to is not None:
            query = query.filter(Workout.planned_date <= date_to)

        if min_duration is not None:
            query = query.filter(Workout.duration >= min_duration)

        if max_duration is not None:
            query = query.filter(Workout.duration <= max_duration)

        # Применяем пагинацию на уровне SQL
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)

        return query

    @with_db_session()
    def create(self, db: Session, workout_data: Workout) -> Workout:
        """Создать новую тренировку"""
        # Исключаем id при создании, чтобы БД сама сгенерировала новый ID
        workout_dict = workout_data.model_dump(exclude={"id"})

        # Преобразуем строку даты в объект date (пустая строка → None)
        if "planned_date" in workout_dict:
            workout_dict["planned_date"] = convert_date_string(workout_dict["planned_date"])

        workout = Workout(**workout_dict)
        db.add(workout)
        db.flush()  # Отправляем изменения в БД без коммита (коммит будет в декораторе)
        db.refresh(
            workout
        )  # Обновляем объект из БД (получаем сгенерированный ID и другие значения)

        # Отсоединяем объект от сессии перед возвратом, чтобы он был доступен после закрытия сессии
        db.expunge(workout)
        return workout

    @with_db_session(expunge_all=True)
    def get_all(
        self,
        db: Session,
        user_id: int = None,
        type: GymType | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        min_duration: int | None = None,
        max_duration: int | None = None,
        page: int = 1,
        size: int = 10,
    ) -> list[Workout]:
        """Получить все тренировки с фильтрацией на уровне SQL"""
        query = db.query(Workout)
        query = self._filter_workouts(
            query,
            user_id=user_id,
            type=type,
            date_from=date_from,
            date_to=date_to,
            min_duration=min_duration,
            max_duration=max_duration,
            page=page,
            size=size,
        )
        workouts = query.all()
        # expunge_all вызывается автоматически декоратором
        return workouts

    @with_db_session()
    def get_by_id(self, db: Session, workout_id: int) -> Workout | None:
        """Получить тренировку по ID"""
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db.expunge(workout)
        return workout

    @with_db_session()
    def update(self, db: Session, workout_id: int, workout_data: Workout) -> Workout | None:
        """Обновить тренировку"""
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            # Исключаем id при обновлении, чтобы не менять ID записи
            workout_dict = workout_data.model_dump(exclude={"id"})

            # Преобразуем строку даты в объект date (пустая строка → None)
            if "planned_date" in workout_dict:
                workout_dict["planned_date"] = convert_date_string(workout_dict["planned_date"])

            # Обновляем поля объекта
            for key, value in workout_dict.items():
                setattr(workout, key, value)

            db.flush()  # Отправляем изменения в БД без коммита (коммит будет в декораторе)
            db.refresh(workout)
            # Отсоединяем объект от сессии перед возвратом, чтобы он был доступен после закрытия сессии
            db.expunge(workout)
            return workout
        return None

    @with_db_session()
    def delete(self, db: Session, workout_id: int) -> bool:
        """Удалить тренировку"""
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db.delete(workout)
            return True
        return False


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
workout_repository = WorkoutRepository()
