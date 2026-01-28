// API запросы для тренировок

import { baseApi } from "@/shared/api";
import type { Workout } from "@/entities/workout/model";
import type { GetWorkoutsParams } from "./types";

export const workoutsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getWorkouts: build.query<Workout[], GetWorkoutsParams | undefined>({
      query: (params) => ({
        url: "/workouts",
        method: "GET",
        params: params,
      }),
    }),
  }),
});

export const { useGetWorkoutsQuery } = workoutsApi;
