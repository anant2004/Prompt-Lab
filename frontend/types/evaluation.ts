export interface EvaluationScores {
  clarity: number;
  context: number;
  specificity: number;
  structure: number;
  tone: number;
}

export interface EvaluationResponse {
  overall_score: number;
  scores: EvaluationScores;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  improved_prompt: string;
}
