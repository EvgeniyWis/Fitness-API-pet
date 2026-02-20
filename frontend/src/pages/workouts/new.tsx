import Link from "next/link";
import { useRouter } from "next/router";
import React from "react";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";
import type { GymType } from "@/entities/workout/model";
import { useCreateWorkoutMutation } from "@/entities/workout/api";
import { Button, Input } from "@/shared/ui";

export default function NewWorkoutPage() {
  const router = useRouter();
  const isAuthenticated = useSelector(selectIsAuthenticated);

  const [createWorkout, { isLoading, error }] = useCreateWorkoutMutation();

  const [type, setType] = React.useState<GymType>("gym");
  const [plannedDate, setPlannedDate] = React.useState<string>("");
  const [duration, setDuration] = React.useState<string>("");
  const [repetitions, setRepetitions] = React.useState<string>("");
  const [exercisesText, setExercisesText] = React.useState<string>("");
  const [notes, setNotes] = React.useState<string>("");
  const [touched, setTouched] = React.useState<Record<string, boolean>>({});
  const [submitAttempted, setSubmitAttempted] = React.useState(false);

  const durationNum = duration.trim() === "" ? NaN : Number(duration);
  const repetitionsNum = repetitions.trim() === "" ? NaN : Number(repetitions);

  const errors = {
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
  const canSubmit = !isLoading && !hasErrors;

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

    await createWorkout({
      type,
      duration: durationNum,
      repetitions: repetitionsNum,
      planned_date: plannedDate.trim() ? plannedDate : null,
      notes: notes.trim() || null,
      exercises,
    }).unwrap();
    await router.push("/workouts");
  };

  if (!isAuthenticated) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl font-bold text-gray-900">Новая тренировка</h1>
        <p className="text-sm text-gray-700">
          Чтобы создать тренировку, нужно{" "}
          <Link href="/login" className="font-medium underline">
            войти
          </Link>
          .
        </p>
        <Link href="/workouts" className="text-sm font-medium underline">
          Вернуться к списку тренировок
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Новая тренировка</h1>
          <p className="mt-1 text-sm text-gray-600">
            Создание (POST /workouts)
          </p>
        </div>
        <Link href="/workouts">
          <Button variant="outline" size="md" type="button">
            Отмена
          </Button>
        </Link>
      </div>

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
              setTouched((t) => ({ ...t, duration: true }));
            }}
            onBlur={() => setTouched((t) => ({ ...t, duration: true }))}
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
              setTouched((t) => ({ ...t, repetitions: true }));
            }}
            onBlur={() => setTouched((t) => ({ ...t, repetitions: true }))}
            placeholder="Например, 10"
            error={submitAttempted || touched.repetitions ? errors.repetitions ?? undefined : undefined}
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

        {error && "data" in error ? (() => {
          const msg = String(error);
          return msg ? (
            <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
              {msg}
            </div>
          ) : null;
        })() : null}

        <p className="text-xs text-gray-500">* — обязательные поля</p>

        <div className="flex items-center justify-end gap-3">
          <Button
            variant="primary"
            size="md"
            type="submit"
            disabled={!canSubmit}
          >
            {isLoading ? "Создание…" : "Создать"}
          </Button>
        </div>
      </form>
    </div>
  );
}
