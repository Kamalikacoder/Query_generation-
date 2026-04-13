import { removeStopwords } from "stopword";
import natural from "natural";

const tokenizer = new natural.WordTokenizer();

/**
 * Cleans text by converting to lowercase and removing extra punctuation.
 */
export const cleanText = (text: string): string => {
  return text
    .toLowerCase()
    .replace(/[^\w\s]/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
};

/**
 * Extracts keywords from a medical claim.
 * Removes stopwords and keeps meaningful tokens.
 */
export const extractKeywords = (text: string): string[] => {
  const cleaned = cleanText(text);
  const tokens = tokenizer.tokenize(cleaned) || [];
  
  // Remove common English stopwords
  const filtered = removeStopwords(tokens);
  
  // Remove duplicates and very short words (unless they look like medical abbreviations)
  const uniqueKeywords = Array.from(new Set(filtered)).filter(
    (word) => word.length > 2 || /^[a-z]\d+$/i.test(word) // e.g., T1, B12
  );
  
  return uniqueKeywords;
};

/**
 * Formats keywords into a PubMed-style query.
 */
export const formatPubMedQuery = (keywords: string[]): string => {
  return keywords.join(" ");
};
