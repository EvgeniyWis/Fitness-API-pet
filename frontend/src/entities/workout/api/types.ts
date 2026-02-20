export interface GetWorkoutsParams {
  type?: "gym" | "volleyball";
  date_from?: string; // YYYY-MM-DD
  date_to?: string; // YYYY-MM-DD
  min_duration?: number;
  max_duration?: number;
  page?: number;
  size?: number;
}

export interface CreateWorkoutRequest {
  type: "gym" | "volleyball";
  duration: number;
  repetitions: number;
  planned_date?: string | null; // YYYY-MM-DD
  notes?: string | null;
  exercises?: string[] | null;
}

export interface UpdateWorkoutRequest {
  type: "gym" | "volleyball";
  duration: number;
  repetitions: number;
  planned_date?: string | null; // YYYY-MM-DD
  notes?: string | null;
  exercises?: string[] | null;
}
