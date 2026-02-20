// API запросы для тренировок

import { baseApi } from "@/shared/api";
import type { Workout } from "@/entities/workout/model";
import type { CreateWorkoutRequest, GetWorkoutsParams } from "./types";

export const workoutsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getWorkouts: build.query<Workout[], GetWorkoutsParams | undefined>({
      query: (params) => ({
        url: "/workouts",
        method: "GET",
        params: params,
      }),
    }),
    createWorkout: build.mutation<Workout, CreateWorkoutRequest>({
      query: (body) => ({
        url: "/workouts",
        method: "POST",
        body,
      }),
      invalidatesTags: [{ type: "Workout", id: "LIST" }],
    }),
  }),
});

export const { useGetWorkoutsQuery, useCreateWorkoutMutation } = workoutsApi;
