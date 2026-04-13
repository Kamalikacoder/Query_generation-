import { z } from "zod";

export const generateQuerySchema = z.object({
  claim: z
    .string()
    .trim()
    .min(1, "Claim must be a non-empty string"),
});
