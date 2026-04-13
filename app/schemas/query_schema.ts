import { z } from "zod";

/**
 * Schema for the query generation request.
 */
export const QueryRequestSchema = z.object({
  claim: z.string().min(1, "Claim cannot be empty").min(5, "Claim is too short to be a valid medical statement"),
});

export type QueryRequest = z.infer<typeof QueryRequestSchema>;

/**
 * Schema for the query generation response data.
 */
export const QueryResponseDataSchema = z.object({
  claim: z.string(),
  keywords: z.array(z.string()),
  primary_query: z.string(),
  alternate_queries: z.array(z.string()),
});

export type QueryResponseData = z.infer<typeof QueryResponseDataSchema>;

/**
 * Schema for the full API response.
 */
export const ApiResponseSchema = z.object({
  success: z.boolean(),
  message: z.string(),
  data: QueryResponseDataSchema.optional(),
});

export type ApiResponse = z.infer<typeof ApiResponseSchema>;
