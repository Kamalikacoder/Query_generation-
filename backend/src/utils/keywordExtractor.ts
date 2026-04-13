import natural from "natural";
import { removeStopwords } from "stopword";

const tokenizer = new natural.WordTokenizer();

export const extractKeywords = (text: string): string[] => {
  const cleanClaim = text.trim().toLowerCase();
  const tokens = tokenizer.tokenize(cleanClaim);

  const filteredTokens = removeStopwords(tokens).filter((word) => {
    return word.length > 2 || /^[a-z]\d+$/i.test(word);
  });

  const uniq = Array.from(new Set(filteredTokens));

  if (uniq.length === 0) {
    return tokens
      .filter((word) => word.length > 2)
      .map((word) => word.toLowerCase());
  }

  return uniq;
};
