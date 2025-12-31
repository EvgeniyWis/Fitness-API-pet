from typing import Optional
from app.models.workout import Workout
from app.core.database import get_db_session
from app.utils.date_utils import convert_date_string


class WorkoutRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""
    def create(self, workout_data: Workout) -> Workout:
        """Создать новую тренировку"""
        with get_db_session() as db:
            # Исключаем id при создании, чтобы БД сама сгенерировала новый ID
            workout_dict = workout_data.model_dump(exclude={'id'})

            # Преобразуем строку даты в объект date
            if 'planned_date' in workout_dict and workout_dict['planned_date'] is not None:
                workout_dict['planned_date'] = convert_date_string(workout_dict['planned_date'])

            workout = Workout(**workout_dict)
            db.add(workout)
            db.flush()  # Отправляем изменения в БД без коммита (коммит будет в контекстном менеджере)
            db.refresh(workout)  # Обновляем объект из БД (получаем сгенерированный ID и другие значения)
            # Отсоединяем объект от сессии перед возвратом, чтобы он был доступен после закрытия сессии
            db.expunge(workout)
            return workout
    
    def get_all(self) -> list[Workout]:
        """Получить все тренировки"""
        with get_db_session() as db:
            workouts = db.query(Workout).all()
            # Отсоединяем все объекты от сессии перед возвратом, чтобы они были доступны после закрытия сессии
            db.expunge_all()
            return workouts
    
    def get_by_id(self, workout_id: int) -> Optional[Workout]:
        """Получить тренировку по ID"""
        with get_db_session() as db:
            workout = db.query(Workout).filter(Workout.id == workout_id).first()
            db.expunge(workout)
            return workout
    
    def update(self, workout_id: int, workout_data: Workout) -> Optional[Workout]:
        """Обновить тренировку"""
        with get_db_session() as db:
            workout = db.query(Workout).filter(Workout.id == workout_id).first()
            if workout:
                # Исключаем id при обновлении, чтобы не менять ID записи
                workout_dict = workout_data.model_dump(exclude={'id'})
                    
                # Обновляем поля объекта
                for key, value in workout_dict.items():
                    setattr(workout, key, value)

                db.flush()  # Отправляем изменения в БД без коммита (коммит будет в контекстном менеджере)
                db.refresh(workout)
                # Отсоединяем объект от сессии перед возвратом, чтобы он был доступен после закрытия сессии
                db.expunge(workout)
                return workout
        return None
    
    def delete(self, workout_id: int) -> bool:
        """Удалить тренировку"""
        with get_db_session() as db:
            workout = db.query(Workout).filter(Workout.id == workout_id).first()
            if workout:
                db.delete(workout)
                return True
            return False


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
workout_repository = WorkoutRepository()

