import Link from "next/link";
import { useRouter } from "next/router";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";
import { WorkoutList } from "@/widgets/workout/workout-list/ui";
import { Button } from "@/shared/ui";

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

  const minDurationRaw = getQueryParam("min_duration");
  const maxDurationRaw = getQueryParam("max_duration");

  const parseOptionalInt = (s: string | undefined): number | undefined => {
    if (s === undefined || s.trim() === "") return undefined;
    const n = Number.parseInt(s, 10);
    return Number.isFinite(n) ? n : undefined;
  };
  const minDuration = parseOptionalInt(minDurationRaw);
  const maxDuration = parseOptionalInt(maxDurationRaw);

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
      min_duration = minDurationRaw ?? "",
      max_duration = maxDurationRaw ?? "",
    } = overrides;

    const query: Record<string, string> = {};

    if (page && page !== "1") query.page = page;
    if (type) query.type = type;
    if (date_from) query.date_from = date_from;
    if (date_to) query.date_to = date_to;
    const minNum = min_duration === "" ? NaN : Number(min_duration);
    const maxNum = max_duration === "" ? NaN : Number(max_duration);
    if (Number.isFinite(minNum)) query.min_duration = String(minNum);
    if (Number.isFinite(maxNum)) query.max_duration = String(maxNum);

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
    pushWithQuery({
      page: "1",
      min_duration: value.trim(),
    });
  };

  const handleMaxDurationChange = (value: string) => {
    pushWithQuery({
      page: "1",
      max_duration: value.trim(),
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

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <Link href="/workouts/new">
              <Button variant="primary" size="md">
                Создать тренировку
              </Button>
            </Link>
          ) : (
            <div className="text-sm text-gray-700">
              Чтобы увидеть тренировки, нужно{" "}
              <Link href="/login" className="font-medium underline">
                войти
              </Link>
              .
            </div>
          )}
        </div>
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
        minDuration={minDuration ?? undefined}
        maxDuration={maxDuration ?? undefined}
      />
    </div>
  );
}
