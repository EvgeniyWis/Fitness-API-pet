import Link from "next/link";
import { useRouter } from "next/router";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";
import { useGetWorkoutQuery, useUpdateWorkoutMutation } from "@/entities/workout/api";
import { WorkoutForm } from "@/entities/workout/ui";
import { Button } from "@/shared/ui";

export default function EditWorkoutPage() {
  const router = useRouter();
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const workoutId = router.query.id as string | undefined;
  const workoutIdNum = workoutId ? Number.parseInt(workoutId, 10) : NaN;

  const {
    data: workout,
    isLoading: isLoadingWorkout,
    error: loadError,
  } = useGetWorkoutQuery(workoutIdNum, {
    skip: !workoutId || Number.isNaN(workoutIdNum),
  });

  const [updateWorkout, { isLoading: isUpdating, error: updateError }] =
    useUpdateWorkoutMutation();

  const handleSubmit = async (values: Parameters<typeof updateWorkout>[0]["data"]) => {
    if (!workout) return;
    await updateWorkout({
      id: workout.id,
      data: values,
    }).unwrap();
    await router.push("/workouts");
  };

  if (!isAuthenticated) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl font-bold text-gray-900">Редактирование тренировки</h1>
        <p className="text-sm text-gray-700">
          Чтобы редактировать тренировку, нужно{" "}
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

  if (!workoutId || Number.isNaN(workoutIdNum)) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl font-bold text-gray-900">Редактирование тренировки</h1>
        <p className="text-sm text-red-600">Неверный ID тренировки</p>
        <Link href="/workouts" className="text-sm font-medium underline">
          Вернуться к списку тренировок
        </Link>
      </div>
    );
  }

  if (isLoadingWorkout) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl font-bold text-gray-900">Редактирование тренировки</h1>
        <p className="text-sm text-gray-600">Загрузка данных тренировки...</p>
      </div>
    );
  }

  if (loadError || !workout) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl font-bold text-gray-900">Редактирование тренировки</h1>
        <p className="text-sm text-red-600">
          {loadError && "data" in loadError
            ? String(loadError.data) || "Ошибка загрузки тренировки"
            : "Тренировка не найдена"}
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
          <h1 className="text-2xl font-bold text-gray-900">Редактирование тренировки</h1>
          <p className="mt-1 text-sm text-gray-600">
            Редактирование (GET /workouts/{workout.id} → PUT /workouts/{workout.id})
          </p>
        </div>
        <Link href="/workouts">
          <Button variant="outline" size="md" type="button">
            Отмена
          </Button>
        </Link>
      </div>

      <WorkoutForm
        initialValues={
          workout
            ? {
                type: workout.type,
                plannedDate: workout.planned_date || "",
                duration: String(workout.duration),
                repetitions: String(workout.repetitions),
                exercisesText: workout.exercises?.join("\n") || "",
                notes: workout.notes || "",
              }
            : undefined
        }
        onSubmit={handleSubmit}
        isLoading={isUpdating}
        error={updateError}
        submitButtonText="Сохранить"
        submitButtonLoadingText="Сохранение…"
      />
    </div>
  );
}
