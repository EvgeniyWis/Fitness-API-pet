export interface GetWorkoutsParams {
  type?: "gym" | "volleyball";
  date_from?: string; // YYYY-MM-DD
  date_to?: string; // YYYY-MM-DD
  min_duration?: number;
  max_duration?: number;
  page?: number;
  size?: number;
}
