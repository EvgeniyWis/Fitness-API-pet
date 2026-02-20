import Link from "next/link";
import { useRouter } from "next/router";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";
import { useCreateWorkoutMutation } from "@/entities/workout/api";
import { WorkoutForm } from "@/entities/workout/ui";
import { Button } from "@/shared/ui";

export default function NewWorkoutPage() {
  const router = useRouter();
  const isAuthenticated = useSelector(selectIsAuthenticated);

  const [createWorkout, { isLoading, error }] = useCreateWorkoutMutation();

  const handleSubmit = async (values: Parameters<typeof createWorkout>[0]) => {
    await createWorkout(values).unwrap();
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

      <WorkoutForm
        onSubmit={handleSubmit}
        isLoading={isLoading}
        error={error}
        submitButtonText="Создать"
        submitButtonLoadingText="Создание…"
      />
    </div>
  );
}
