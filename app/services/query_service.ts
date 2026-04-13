import { extractKeywords, formatPubMedQuery } from "../utils/text_utils";
import { QueryResponseData } from "../schemas/query_schema";

/**
 * Service logic for generating medical search queries.
 */
export class QueryService {
  /**
   * Generates a primary and alternate queries from a medical claim.
   */
  public static generateQueries(claim: string): QueryResponseData {
    const keywords = extractKeywords(claim);
    const primaryQuery = formatPubMedQuery(keywords);
    
    const alternateQueries: string[] = [];
    
    if (keywords.length >= 2) {
      // Variation 1: "X and Y"
      alternateQueries.push(`${keywords[0]} and ${keywords[1]} ${keywords.slice(2).join(" ")}`.trim());
      
      // Variation 2: "X therapy for Y" (if we have enough keywords)
      if (keywords.length >= 2) {
        alternateQueries.push(`${keywords[0]} therapy for ${keywords[1]}`);
      }
      
      // Variation 3: "X risk in Y"
      alternateQueries.push(`${keywords.slice(1).join(" ")} risk in ${keywords[0]}`.trim());
    } else {
      // Fallback for very short claims
      alternateQueries.push(`${primaryQuery} medical study`);
      alternateQueries.push(`clinical evidence for ${primaryQuery}`);
    }

    return {
      claim,
      keywords,
      primary_query: primaryQuery,
      alternate_queries: Array.from(new Set(alternateQueries)).slice(0, 3),
    };
  }
}
