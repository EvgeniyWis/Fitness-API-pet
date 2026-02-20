import React from "react";
import type { GymType } from "@/entities/workout/model";
import { Button, Input } from "@/shared/ui";
import { useWorkoutForm } from "./use-workout-form";
import type { CreateWorkoutRequest, UpdateWorkoutRequest } from "@/entities/workout/api/types";

/** Ошибка API (например, от RTK Query mutation), у которой может быть поле data. */
export type WorkoutFormApiError =
  | { data?: unknown }
  | { status?: number; data?: unknown }
  | { name?: string; message?: string; code?: string }
  | null
  | undefined;

export interface WorkoutFormProps {
  initialValues?: {
    type?: GymType;
    plannedDate?: string;
    duration?: string;
    repetitions?: string;
    exercisesText?: string;
    notes?: string;
  };
  onSubmit: (values: CreateWorkoutRequest | UpdateWorkoutRequest) => Promise<void>;
  isLoading?: boolean;
  error?: WorkoutFormApiError;
  submitButtonText?: string;
  submitButtonLoadingText?: string;
}

export const WorkoutForm: React.FC<WorkoutFormProps> = ({
  initialValues,
  onSubmit,
  isLoading = false,
  error,
  submitButtonText = "Сохранить",
  submitButtonLoadingText = "Сохранение…",
}) => {
  const {
    type,
    plannedDate,
    duration,
    repetitions,
    exercisesText,
    notes,
    setType,
    setPlannedDate,
    setDuration,
    setRepetitions,
    setExercisesText,
    setNotes,
    errors,
    hasErrors,
    touched,
    submitAttempted,
    markFieldTouched,
    handleSubmit,
  } = useWorkoutForm({
    initialValues,
    onSubmit,
  });

  const canSubmit = !isLoading && !hasErrors;

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-lg border border-gray-200 bg-white p-4 space-y-4"
    >
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="space-y-1">
          <label className="block text-sm font-medium text-gray-700">
            Тип тренировки
          </label>
          <select
            className="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={type}
            onChange={(e) => setType(e.target.value as GymType)}
          >
            <option value="gym">Тренажёрный зал</option>
            <option value="volleyball">Волейбол</option>
          </select>
        </div>

        <Input
          type="date"
          label="Запланированная дата"
          value={plannedDate}
          onChange={(e) => setPlannedDate(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <Input
          type="number"
          min={1}
          label="Длительность (мин) *"
          value={duration}
          onChange={(e) => {
            setDuration(e.target.value);
            markFieldTouched("duration");
          }}
          onBlur={() => markFieldTouched("duration")}
          placeholder="Например, 60"
          error={submitAttempted || touched.duration ? errors.duration ?? undefined : undefined}
        />
        <Input
          type="number"
          min={0}
          label="Повторения *"
          value={repetitions}
          onChange={(e) => {
            setRepetitions(e.target.value);
            markFieldTouched("repetitions");
          }}
          onBlur={() => markFieldTouched("repetitions")}
          placeholder="Например, 10"
          error={
            submitAttempted || touched.repetitions ? errors.repetitions ?? undefined : undefined
          }
        />
      </div>

      <div className="space-y-1">
        <label className="block text-sm font-medium text-gray-700">
          Упражнения (по одному в строке или через запятую)
        </label>
        <textarea
          className="block w-full min-h-[96px] rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={exercisesText}
          onChange={(e) => setExercisesText(e.target.value)}
          placeholder={"Присед\nЖим лёжа\nТяга"}
        />
      </div>

      <div className="space-y-1">
        <label className="block text-sm font-medium text-gray-700">
          Заметки
        </label>
        <textarea
          className="block w-full min-h-[96px] rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Любые детали тренировки…"
        />
      </div>

      {error && "data" in error && error.data != null ? (() => {
        const msg = String(error.data);
        return msg ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
            {msg}
          </div>
        ) : null;
      })() : null}

      <p className="text-xs text-gray-500">* — обязательные поля</p>

      <div className="flex items-center justify-end gap-3">
        <Button variant="primary" size="md" type="submit" disabled={!canSubmit}>
          {isLoading ? submitButtonLoadingText : submitButtonText}
        </Button>
      </div>
    </form>
  );
};
