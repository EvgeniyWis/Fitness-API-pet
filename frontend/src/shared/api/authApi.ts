import { baseApi } from "./baseApi";

/** Тело запроса на регистрацию (совпадает с backend User без id) */
export interface RegisterRequest {
  username: string;
  password: string;
  role?: "admin" | "user";
}

export interface RegisterResponse {
  message: string;
}

/** Тело запроса на вход */
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  access_token?: string;
  refresh_token?: string;
}

export interface RefreshResponse {
  message?: string;
  access_token?: string;
  refresh_token?: string;
}

export const authApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    register: build.mutation<RegisterResponse, RegisterRequest>({
      query: (body) => ({
        url: "/auth/register",
        method: "POST",
        body,
      }),
    }),
    login: build.mutation<LoginResponse, LoginRequest>({
      query: (body) => ({
        url: "/auth/login",
        method: "POST",
        body,
      }),
    }),
    logout: build.mutation<unknown, void>({
      query: () => ({
        url: "/auth/logout",
        method: "POST",
      }),
    }),
    refresh: build.mutation<RefreshResponse, void>({
      query: () => ({
        url: "/auth/refresh",
        method: "POST",
      }),
    }),
  }),
});

export const {
  useRegisterMutation,
  useLoginMutation,
  useLogoutMutation,
  useRefreshMutation,
} = authApi;
