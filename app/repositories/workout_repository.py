from typing import Optional
from app.models.workout import Workout
from app.utils.date_utils import convert_date_string
from app.utils.db_decorator import with_db_session
from sqlalchemy.orm import Session


class WorkoutRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""
    @with_db_session()
    def create(self, db: Session, workout_data: Workout) -> Workout:
        """Создать новую тренировку"""
        # Исключаем id при создании, чтобы БД сама сгенерировала новый ID
        workout_dict = workout_data.model_dump(exclude={'id'})

        # Преобразуем строку даты в объект date
        if 'planned_date' in workout_dict and workout_dict['planned_date'] is not None:
            workout_dict['planned_date'] = convert_date_string(workout_dict['planned_date'])

        workout = Workout(**workout_dict)
        db.add(workout)
        db.flush()  # Отправляем изменения в БД без коммита (коммит будет в декораторе)
        db.refresh(workout)  # Обновляем объект из БД (получаем сгенерированный ID и другие значения)
        # Отсоединяем объект от сессии перед возвратом, чтобы он был доступен после закрытия сессии
        db.expunge(workout)
        return workout
    
    @with_db_session(expunge_all=True)
    def get_all(self, db: Session) -> list[Workout]:
        """Получить все тренировки"""
        workouts = db.query(Workout).all()
        # expunge_all вызывается автоматически декоратором
        return workouts
    
    @with_db_session()
    def get_by_id(self, db: Session, workout_id: int) -> Optional[Workout]:
        """Получить тренировку по ID"""
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db.expunge(workout)
        return workout
    
    @with_db_session()
    def update(self, db: Session, workout_id: int, workout_data: Workout) -> Optional[Workout]:
        """Обновить тренировку"""
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            # Исключаем id при обновлении, чтобы не менять ID записи
            workout_dict = workout_data.model_dump(exclude={'id'})
            
            # Преобразуем строку даты в объект date
            if 'planned_date' in workout_dict and workout_dict['planned_date'] is not None:
                workout_dict['planned_date'] = convert_date_string(workout_dict['planned_date'])
                
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

