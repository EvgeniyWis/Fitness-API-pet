import Link from "next/link";
import { useRouter } from "next/router";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";
import { WorkoutList } from "@/widgets/workout/workout-list/ui";

export default function WorkoutsPage() {
  const router = useRouter();
  const isAuthenticated = useSelector(selectIsAuthenticated);

  const getQueryParam = (name: string): string | undefined => {
    const value = router.query[name] as string;

    if (!value) return;
    return value;
  };

  const pageFromQuery = getQueryParam("page");
  const currentPage = pageFromQuery
    ? Math.max(1, Number.parseInt(pageFromQuery, 10))
    : 1;

  const typeFilter = getQueryParam("type") as "gym" | "volleyball";
  const dateFrom = getQueryParam("date_from");
  const dateTo = getQueryParam("date_to");

  const minDurationRaw = getQueryParam("min_duration")!;
  const maxDurationRaw = getQueryParam("max_duration")!;

  const minDuration = Number.parseInt(minDurationRaw, 10);

  const maxDuration = Number.parseInt(maxDurationRaw, 10);

  const buildQuery = (overrides: {
    page?: string;
    type?: string;
    date_from?: string;
    date_to?: string;
    min_duration?: string;
    max_duration?: string;
  }) => {
    const {
      page = String(currentPage),
      type = typeFilter,
      date_from = dateFrom,
      date_to = dateTo,
      min_duration = minDurationRaw,
      max_duration = maxDurationRaw,
    } = overrides;

    const query: Record<string, string> = {};

    if (page && page !== "1") query.page = page;
    if (type) query.type = type;
    if (date_from) query.date_from = date_from;
    if (date_to) query.date_to = date_to;
    if (min_duration) query.min_duration = min_duration;
    if (max_duration) query.max_duration = max_duration;

    return query;
  };

  const pushWithQuery = (overrides: {
    page?: string;
    type?: string;
    date_from?: string;
    date_to?: string;
    min_duration?: string;
    max_duration?: string;
  }) => {
    const query = buildQuery(overrides);

    router.push({
      pathname: "/workouts",
      query,
    });
  };

  const handlePageChange = (nextPage: number) => {
    pushWithQuery({ page: String(nextPage) });
  };

  const handleTypeChange = (value: string) => {
    pushWithQuery({
      page: "1",
      type: value,
    });
  };

  const handleDateFromChange = (value: string) => {
    pushWithQuery({
      page: "1",
      date_from: value || undefined,
    });
  };

  const handleDateToChange = (value: string) => {
    pushWithQuery({
      page: "1",
      date_to: value || undefined,
    });
  };

  const handleMinDurationChange = (value: string) => {
    const trimmed = value.trim();

    pushWithQuery({
      page: "1",
      min_duration: trimmed || undefined,
    });
  };

  const handleMaxDurationChange = (value: string) => {
    const trimmed = value.trim();

    pushWithQuery({
      page: "1",
      max_duration: trimmed || undefined,
    });
  };

  const handleResetFilters = () => {
    router.push({
      pathname: "/workouts",
      query: {},
    });
  };

  const PAGE_SIZE = 10;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Тренировки</h1>
          <p className="mt-1 text-sm text-gray-600">
            Список всех тренировок текущего пользователя (GET /workouts)
          </p>
        </div>

        {!isAuthenticated ? (
          <div className="text-sm text-gray-700">
            Чтобы увидеть тренировки, нужно{" "}
            <Link href="/login" className="font-medium underline">
              войти
            </Link>
            .
          </div>
        ) : null}
      </div>

      {isAuthenticated ? (
        <div className="rounded-lg border border-gray-200 bg-white p-4 space-y-3">
          <div className="flex items-center justify-between gap-2">
            <h2 className="text-sm font-medium text-gray-900">
              Фильтры тренировок
            </h2>
            <button
              type="button"
              onClick={handleResetFilters}
              className="text-xs text-gray-500 underline hover:text-gray-700"
            >
              Сбросить
            </button>
          </div>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <div className="space-y-1">
              <label className="block text-xs font-medium text-gray-700">
                Тип тренировки
              </label>
              <select
                className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                value={typeFilter ?? ""}
                onChange={(e) => handleTypeChange(e.target.value)}
              >
                <option value="">Все типы</option>
                <option value="gym">Тренажёрный зал</option>
                <option value="volleyball">Волейбол</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-medium text-gray-700">
                Дата с
              </label>
              <input
                type="date"
                className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                value={dateFrom ?? ""}
                onChange={(e) => handleDateFromChange(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-medium text-gray-700">
                Дата по
              </label>
              <input
                type="date"
                className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                value={dateTo ?? ""}
                onChange={(e) => handleDateToChange(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-medium text-gray-700">
                Мин. длительность (мин)
              </label>
              <input
                type="number"
                min={0}
                className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                value={minDurationRaw ?? ""}
                onChange={(e) => handleMinDurationChange(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-medium text-gray-700">
                Макс. длительность (мин)
              </label>
              <input
                type="number"
                min={0}
                className="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                value={maxDurationRaw ?? ""}
                onChange={(e) => handleMaxDurationChange(e.target.value)}
              />
            </div>
          </div>
        </div>
      ) : null}

      <WorkoutList
        page={currentPage}
        pageSize={PAGE_SIZE}
        onPageChange={handlePageChange}
        typeFilter={typeFilter}
        dateFrom={dateFrom}
        dateTo={dateTo}
        minDuration={minDuration}
        maxDuration={maxDuration}
      />
    </div>
  );
}
