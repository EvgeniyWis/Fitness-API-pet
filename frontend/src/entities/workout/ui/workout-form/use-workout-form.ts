import React from "react";
import type { GymType } from "@/entities/workout/model";
import type { CreateWorkoutRequest, UpdateWorkoutRequest } from "@/entities/workout/api/types";

export interface WorkoutFormValues {
  type: GymType;
  plannedDate: string;
  duration: string;
  repetitions: string;
  exercisesText: string;
  notes: string;
}

export interface WorkoutFormErrors {
  duration: string | null;
  repetitions: string | null;
}

export interface UseWorkoutFormOptions {
  initialValues?: Partial<WorkoutFormValues>;
  onSubmit: (values: CreateWorkoutRequest | UpdateWorkoutRequest) => Promise<void>;
}

export function useWorkoutForm({ initialValues, onSubmit }: UseWorkoutFormOptions) {
  const [type, setType] = React.useState<GymType>(initialValues?.type || "gym");
  const [plannedDate, setPlannedDate] = React.useState<string>(initialValues?.plannedDate || "");
  const [duration, setDuration] = React.useState<string>(initialValues?.duration || "");
  const [repetitions, setRepetitions] = React.useState<string>(initialValues?.repetitions || "");
  const [exercisesText, setExercisesText] = React.useState<string>(
    initialValues?.exercisesText || "",
  );
  const [notes, setNotes] = React.useState<string>(initialValues?.notes || "");
  const [touched, setTouched] = React.useState<Record<string, boolean>>({});
  const [submitAttempted, setSubmitAttempted] = React.useState(false);

  // Обновляем значения при изменении initialValues
  React.useEffect(() => {
    if (initialValues) {
      if (initialValues.type !== undefined) setType(initialValues.type);
      if (initialValues.plannedDate !== undefined) setPlannedDate(initialValues.plannedDate);
      if (initialValues.duration !== undefined) setDuration(initialValues.duration);
      if (initialValues.repetitions !== undefined) setRepetitions(initialValues.repetitions);
      if (initialValues.exercisesText !== undefined) setExercisesText(initialValues.exercisesText);
      if (initialValues.notes !== undefined) setNotes(initialValues.notes);
    }
  }, [initialValues]);

  const durationNum = duration.trim() === "" ? NaN : Number(duration);
  const repetitionsNum = repetitions.trim() === "" ? NaN : Number(repetitions);

  const errors: WorkoutFormErrors = {
    duration:
      duration.trim() === ""
        ? "Укажите длительность"
        : !Number.isFinite(durationNum) || durationNum < 1
          ? "Длительность должна быть не меньше 1 минуты"
          : null,
    repetitions:
      repetitions.trim() === ""
        ? "Укажите количество повторений"
        : !Number.isFinite(repetitionsNum) || repetitionsNum < 0
          ? "Число повторений не может быть отрицательным"
          : null,
  };

  const hasErrors = Boolean(errors.duration || errors.repetitions);

  const parseExercises = (raw: string): string[] => {
    const trimmed = raw.trim();
    return trimmed
      .split(/\r?\n|,/g)
      .map((s) => s.trim())
      .filter(Boolean);
  };

  const handleSubmit = async (evt: React.FormEvent) => {
    evt.preventDefault();
    setSubmitAttempted(true);
    if (hasErrors) return;

    const exercises = parseExercises(exercisesText);

    await onSubmit({
      type,
      duration: durationNum,
      repetitions: repetitionsNum,
      planned_date: plannedDate.trim() ? plannedDate : null,
      notes: notes.trim() || null,
      exercises,
    });
  };

  const markFieldTouched = (fieldName: string) => {
    setTouched((t) => ({ ...t, [fieldName]: true }));
  };

  return {
    // Значения
    type,
    plannedDate,
    duration,
    repetitions,
    exercisesText,
    notes,
    // Сеттеры
    setType,
    setPlannedDate,
    setDuration,
    setRepetitions,
    setExercisesText,
    setNotes,
    // Валидация
    errors,
    hasErrors,
    touched,
    submitAttempted,
    markFieldTouched,
    // Обработчики
    handleSubmit,
  };
}
