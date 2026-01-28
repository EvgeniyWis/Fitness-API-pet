import { useRouter } from "next/router";
import { useLogoutMutation } from "@/shared/api";
import { useAppDispatch } from "@/app/store";
import { baseApi } from "@/shared/api";

export const useAuthFlow = () => {
  const router = useRouter();
  const dispatch = useAppDispatch();
  const [logout] = useLogoutMutation();

  const handleLogout = async () => {
    await logout();
    dispatch(baseApi.util.resetApiState());
    router.push("/login");
  };

  return { handleLogout };
};
