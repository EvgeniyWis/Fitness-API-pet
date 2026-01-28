// Модель тренировки (типы, интерфейсы)

export type GymType = "gym" | "volleyball";

export interface Workout {
  id: number;
  user_id: number | null;
  type: GymType;
  duration: number;
  repetitions: number;
  planned_date: string | null;
  notes: string | null;
  exercises: string[] | null;
}
