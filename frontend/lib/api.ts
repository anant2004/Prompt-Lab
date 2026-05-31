import { EvaluationResponse } from "@/types/evaluation";

const apiUrlFromEnv = process.env.NEXT_PUBLIC_API_URL?.trim();
const API_URL = (apiUrlFromEnv || "http://localhost:8000").replace(/\/$/, "");
const EVALUATE_URL = `${API_URL}/api/evaluate`;

const mockResponse = (inputPrompt: string): EvaluationResponse => ({
  overall_score: 76,
  scores: {
    clarity: 79,
    context: 70,
    specificity: 74,
    structure: 81,
    tone: 76
  },
  strengths: [
    "Prompt has a clear core objective.",
    "Tone is mostly professional and easy to understand."
  ],
  weaknesses: [
    "Context is limited, making assumptions difficult for the model.",
    "Constraints and expected output format are not explicit."
  ],
  suggestions: [
    "Add target audience and scenario details.",
    "Specify response format (e.g., bullet list, JSON, or table).",
    "Define constraints such as word count, style, or deadlines."
  ],
  improved_prompt: `You are an expert assistant helping with this request: "${inputPrompt}".\n\nProvide a structured response with:\n1) concise answer,\n2) key assumptions,\n3) action steps,\n4) final checklist.\n\nKeep the tone professional, limit to 250 words, and use bullet points where appropriate.`
});

export async function evaluatePrompt(prompt: string): Promise<EvaluationResponse> {
  const response = await fetch(EVALUATE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt })
  });

  if (response.ok) {
    return (await response.json()) as EvaluationResponse;
  }

  return mockResponse(prompt);
}
