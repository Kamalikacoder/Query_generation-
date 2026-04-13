export interface GenerateQueryRequest {
  claim: string;
}

export interface QueryResult {
  originalClaim: string;
  cleanedClaim: string;
  generatedQuery: string;
  keywords: string[];
  message: string;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}
