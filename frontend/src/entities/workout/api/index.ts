// API запросы для тренировок

import { baseApi } from "@/shared/api";
import type { Workout } from "@/entities/workout/model";
import type { CreateWorkoutRequest, GetWorkoutsParams, UpdateWorkoutRequest } from "./types";

export const workoutsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getWorkouts: build.query<Workout[], GetWorkoutsParams | undefined>({
      query: (params) => ({
        url: "/workouts",
        method: "GET",
        params: params,
      }),
      providesTags: [{ type: "Workout", id: "LIST" }],
    }),
    getWorkout: build.query<Workout, number>({
      query: (id) => ({
        url: `/workouts/${id}`,
        method: "GET",
      }),
      providesTags: (_, _2, id) => [{ type: "Workout", id }],
    }),
    createWorkout: build.mutation<Workout, CreateWorkoutRequest>({
      query: (body) => ({
        url: "/workouts",
        method: "POST",
        body,
      }),
      invalidatesTags: [{ type: "Workout", id: "LIST" }],
    }),
    updateWorkout: build.mutation<Workout, { id: number; data: UpdateWorkoutRequest }>({
      query: ({ id, data }) => ({
        url: `/workouts/${id}`,
        method: "PUT",
        body: data,
      }),
      invalidatesTags: (_, _2, { id }) => [
        { type: "Workout", id },
        { type: "Workout", id: "LIST" },
      ],
    }),
  }),
});

export const {
  useGetWorkoutsQuery,
  useGetWorkoutQuery,
  useCreateWorkoutMutation,
  useUpdateWorkoutMutation,
} = workoutsApi;
