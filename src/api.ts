export interface QueryPayload {
  claim: string;
}

export interface QueryResponseData {
  originalClaim: string;
  cleanedClaim: string;
  generatedQuery: string;
  keywords: string[];
  message: string;
}

interface ApiResponse<T> {
  success: boolean;
  message: string;
  data?: T;
}

const API_BASE_URL = "";

export async function generateSearchQuery(claim: string) {
  const response = await fetch(`/api/query/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ claim }),
  });

  const payload: ApiResponse<QueryResponseData> = await response.json();

  if (!response.ok || !payload.success) {
    throw new Error(payload.message || "Unable to generate query");
  }

  return payload.data;
}
