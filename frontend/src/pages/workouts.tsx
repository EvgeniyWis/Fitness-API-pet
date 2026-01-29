import Link from "next/link";
import { useRouter } from "next/router";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";
import { WorkoutList } from "@/widgets/workout/workout-list/ui";

export default function WorkoutsPage() {
  const router = useRouter();
  const isAuthenticated = useSelector(selectIsAuthenticated);

  const pageParam = router.query.page;
  const pageFromQuery = Array.isArray(pageParam) ? pageParam[0] : pageParam;
  const currentPage =
    pageFromQuery
      ? Math.max(1, Number.parseInt(pageFromQuery, 10))
      : 1;

  const handlePageChange = (nextPage: number) => {
    const query = { page: String(nextPage) };
    router.push(
      {
        pathname: "/workouts",
        query,
      },
    );
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

      <WorkoutList
        page={currentPage}
        pageSize={PAGE_SIZE}
        onPageChange={handlePageChange}
      />
    </div>
  );
}
