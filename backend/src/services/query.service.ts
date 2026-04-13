import { cleanText } from "../utils/textCleaner";
import { extractKeywords } from "../utils/keywordExtractor";
import type { QueryResult } from "../types/query.types";

const addMedicalModifiers = (keywords: string[], cleanedClaim: string): string[] => {
  const modifiers = new Set<string>(["evidence"]);
  const lowerClaim = cleanedClaim.toLowerCase();

  if (/(?:\btreat\b|\bmanage\b|\btherapy\b|\bdrug\b|\bintervention\b|\bcure\b)/.test(lowerClaim)) {
    modifiers.add("treatment");
    modifiers.add("clinical study");
  }

  if (/(?:\brisk\b|\bincidence\b|\bprevalence\b|\bcomplication\b|\bside effect\b)/.test(lowerClaim)) {
    modifiers.add("clinical study");
    modifiers.add("guideline");
  }

  if (/(?:\bdiagnos\b|\bsymptom\b|\bsign\b|\bscreening\b)/.test(lowerClaim)) {
    modifiers.add("evidence");
    modifiers.add("guideline");
  }

  if (keywords.some((word) => /diabetes|hypertension|cancer|infection|asthma|stroke|antibiotic|insulin|antibiotics/.test(word))) {
    modifiers.add("treatment");
  }

  return Array.from(modifiers);
};

export class QueryService {
  public static generateFromClaim(claim: string): QueryResult {
    const cleanedClaim = cleanText(claim);
    const keywords = extractKeywords(cleanedClaim);
    const modifierTerms = addMedicalModifiers(keywords, cleanedClaim);

    const generatedQuery = [...keywords, ...modifierTerms]
      .filter(Boolean)
      .join(" ")
      .replace(/\s+/g, " ")
      .trim();

    return {
      originalClaim: claim,
      cleanedClaim,
      keywords,
      generatedQuery: generatedQuery || cleanedClaim,
      message: "Query generated successfully",
    };
  }
}
