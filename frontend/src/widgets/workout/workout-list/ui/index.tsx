// Виджет списка тренировок
import { useGetWorkoutsQuery } from "@/entities/workout/api";

interface WorkoutListProps {
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}

export const WorkoutList = ({
  page,
  pageSize,
  onPageChange,
}: WorkoutListProps) => {
  const { data, isLoading, isError, refetch } = useGetWorkoutsQuery({
    page,
    size: pageSize,
  });

  if (isLoading) {
    return <div className="text-gray-600">Загрузка тренировок…</div>;
  }

  if (isError) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">
        <div className="font-medium">Ошибка</div>
        <button
          type="button"
          className="mt-3 text-sm font-medium underline"
          onClick={() => refetch()}
        >
          Повторить
        </button>
      </div>
    );
  }

  if (!data || !data.length) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6 text-gray-700">
        Тренировок пока нет.
      </div>
    );
  }

  const hasNextPage = data.length === pageSize;
  const canGoPrev = page > 1;

  return (
    <div className="space-y-4">
      <div className="space-y-3">
        {data.map((w) => (
          <div
            key={w.id}
            className="rounded-lg border border-gray-200 bg-white p-4"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-sm text-gray-500">
                  {w.planned_date ? w.planned_date : "Дата не указана"}
                </div>
                <div className="mt-1 text-lg font-semibold text-gray-900">
                  {w.type === "gym" ? "Тренажёрный зал" : "Волейбол"}
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-500">Длительность</div>
                <div className="text-base font-medium text-gray-900">
                  {w.duration} мин
                </div>
              </div>
            </div>

            <div className="mt-2 grid grid-cols-1 gap-2 text-sm text-gray-700 sm:grid-cols-2">
              <div>
                <span className="text-gray-500">Повторения:</span>{" "}
                <span className="font-medium text-gray-900">
                  {w.repetitions}
                </span>
              </div>
              <div className="sm:text-right">
                <span className="text-gray-500">Упражнений:</span>{" "}
                <span className="font-medium text-gray-900">
                  {Array.isArray(w.exercises) ? w.exercises.length : 0}
                </span>
              </div>
            </div>

            {w.notes ? (
              <div className="mt-3 text-sm text-gray-700">
                <span className="text-gray-500">Заметки:</span> {w.notes}
              </div>
            ) : null}
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-gray-200">
        <button
          type="button"
          className={`px-3 py-1.5 text-sm rounded-md border ${
            canGoPrev
              ? "border-gray-300 text-gray-700 hover:bg-gray-50"
              : "border-gray-200 text-gray-400 cursor-not-allowed"
          }`}
          onClick={() => canGoPrev && onPageChange(page - 1)}
          disabled={!canGoPrev}
        >
          Предыдущая
        </button>

        <span className="text-sm text-gray-600">Страница {page}</span>

        <button
          type="button"
          className={`px-3 py-1.5 text-sm rounded-md border ${
            hasNextPage
              ? "border-gray-300 text-gray-700 hover:bg-gray-50"
              : "border-gray-200 text-gray-400 cursor-not-allowed"
          }`}
          onClick={() => hasNextPage && onPageChange(page + 1)}
          disabled={!hasNextPage}
        >
          Следующая
        </button>
      </div>
    </div>
  );
};
