import { NextFunction, Request, Response } from "express";
import type { ApiResponse } from "../types/query.types";

export const notFoundHandler = (_: Request, res: Response<ApiResponse>) => {
  return res.status(404).json({
    success: false,
    message: "Route not found",
  });
};

export const errorHandler = (
  error: Error,
  _req: Request,
  res: Response<ApiResponse>,
  _next: NextFunction,
) => {
  console.error("Backend error:", error?.message ?? error);
  return res.status(500).json({
    success: false,
    message: "Internal server error",
  });
};
