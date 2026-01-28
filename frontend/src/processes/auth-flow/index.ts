import { useRouter } from "next/router";
import { useEffect } from "react";
import { useLogoutMutation, useRefreshMutation } from "@/shared/api";
import { useAppDispatch } from "@/app/store";
import { baseApi } from "@/shared/api";
import { useSelector } from "react-redux";
import { selectIsAuthenticated } from "@/entities/user/model";

export const useAuthFlow = () => {
  const router = useRouter();
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();
  const [refresh] = useRefreshMutation();
  const isAuthenticated = useSelector(selectIsAuthenticated);

  useEffect(() => {
    if (isAuthenticated) return;
    if (localStorage.getItem("rememberMe") !== "1") return;

    // Пытаемся восстановить сессию по refresh_token cookie
    refresh();
  }, [isAuthenticated, refresh]);

  const handleLogout = async () => {
    await logout();
    dispatch(baseApi.util.resetApiState());
    localStorage.removeItem("rememberMe");
    router.push("/login");
  };

  return { handleLogout };
};
