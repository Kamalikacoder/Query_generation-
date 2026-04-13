import { Request, Response, NextFunction } from "express";
import { generateQuerySchema } from "../validators/query.validator";
import { QueryService } from "../services/query.service";
import type { ApiResponse } from "../types/query.types";

export const generateQueryController = (
  req: Request,
  res: Response<ApiResponse>,
  next: NextFunction,
) => {
  try {
    const parseResult = generateQuerySchema.safeParse(req.body);

    if (!parseResult.success) {
      return res.status(400).json({
        success: false,
        message: parseResult.error.issues[0]?.message ?? "Invalid request payload",
      });
    }

    const result = QueryService.generateFromClaim(parseResult.data.claim);

    return res.json({
      success: true,
      message: "Query generated successfully",
      data: result,
    });
  } catch (error) {
    next(error);
  }
};
