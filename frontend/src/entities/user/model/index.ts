import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "@/app/store";
import { authApi } from "@/shared/api";
import { jwtDecode } from "jwt-decode";

interface UserData {
  sub: string;
  role: string;
  exp: number;
  iat: number;
}

interface UserState {
  isAuthenticated: boolean;
  username: string | null;
  role: string | null;
}

const initialState: UserState = {
  isAuthenticated: false,
  username: null,
  role: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUserData: (
      state,
      action: PayloadAction<{ username: string; role: string }>,
    ) => {
      state.isAuthenticated = true;
      state.username = action.payload.username;
      state.role = action.payload.role;
    },
    clearUserData: (state) => {
      state.isAuthenticated = false;
      state.username = null;
      state.role = null;
    },
  },
  extraReducers: (builder) => {
    builder.addMatcher(
      authApi.endpoints.login.matchFulfilled,
      (state, { payload }) => {
        if (payload.access_token) {
          try {
            const decodedToken = jwtDecode<UserData>(payload.access_token);
            state.isAuthenticated = true;
            state.username = decodedToken.sub;
            state.role = decodedToken.role;
          } catch (error) {
            console.error("Ошибка декодирования токена:", error);
            state.isAuthenticated = false;
            state.username = null;
            state.role = null;
          }
        }
      },
    );
    builder.addMatcher(authApi.endpoints.logout.matchFulfilled, (state) => {
      state.isAuthenticated = false;
      state.username = null;
      state.role = null;
    });
  },
});

export const { setUserData, clearUserData } = userSlice.actions;

export const selectIsAuthenticated = (state: RootState) =>
  state.user.isAuthenticated;
export const selectUsername = (state: RootState) => state.user.username;
export const selectUserRole = (state: RootState) => state.user.role;

export default userSlice.reducer;
