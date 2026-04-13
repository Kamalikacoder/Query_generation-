import { Router, Request, Response } from "express";
import { QueryRequestSchema, ApiResponse } from "../schemas/query_schema";
import { QueryService } from "../services/query_service";

const router = Router();

/**
 * POST /generate-query
 * Generates PubMed queries from a clinical claim.
 */
router.post("/generate-query", (req: Request, res: Response) => {
  try {
    // Validate input
    const validation = QueryRequestSchema.safeParse(req.body);
    
    if (!validation.success) {
      const response: ApiResponse = {
        success: false,
        message: validation.error.issues[0].message,
      };
      return res.status(400).json(response);
    }

    const { claim } = validation.data;
    const result = QueryService.generateQueries(claim);

    const response: ApiResponse = {
      success: true,
      message: "Query generated successfully",
      data: result,
    };

    return res.json(response);
  } catch (error) {
    console.error("Error generating query:", error);
    const response: ApiResponse = {
      success: false,
      message: "An internal server error occurred",
    };
    return res.status(500).json(response);
  }
});

export default router;
