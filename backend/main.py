import json
import os
import re
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "Prompt Lab")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

client = None
if OPENAI_API_KEY:
  default_headers = {}
  if OPENROUTER_SITE_URL:
    default_headers["HTTP-Referer"] = OPENROUTER_SITE_URL
  if OPENROUTER_APP_NAME:
    default_headers["X-Title"] = OPENROUTER_APP_NAME

  client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    default_headers=default_headers
  )


class PromptRequest(BaseModel):
  prompt: str = Field(min_length=5, max_length=5000)


class ScoreBreakdown(BaseModel):
  clarity: int
  context: int
  specificity: int
  structure: int
  tone: int


class EvaluationResponse(BaseModel):
  overall_score: int
  scores: ScoreBreakdown
  strengths: List[str]
  weaknesses: List[str]
  suggestions: List[str]
  improved_prompt: str


app = FastAPI(title="Prompt Lab API", version="1.0.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)


def clamp_score(value: int) -> int:
  return max(0, min(100, value))


def contains_constraints(prompt: str) -> bool:
  patterns = [r"\bmax\b", r"\bmin\b", r"\bwithin\b", r"\blimit\b", r"\bexactly\b", r"\bmust\b"]
  return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)


def mentions_output_format(prompt: str) -> bool:
  patterns = [r"\bjson\b", r"\btable\b", r"\bbullet", r"\bmarkdown\b", r"\bformat\b", r"\bsections?\b"]
  return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns)


def vague_word_count(prompt: str) -> int:
  vague_words = ["good", "nice", "better", "optimize", "improve", "something", "stuff", "best"]
  lowered = prompt.lower()
  return sum(lowered.count(word) for word in vague_words)


def apply_rule_adjustments(prompt: str, scores: Dict[str, int]) -> Dict[str, int]:
  adjusted = scores.copy()
  word_count = len(prompt.split())

  if word_count < 10:
    adjusted["clarity"] -= 12
    adjusted["context"] -= 14
    adjusted["specificity"] -= 14
  elif word_count > 180:
    adjusted["structure"] -= 8

  if vague_word_count(prompt) >= 3:
    adjusted["specificity"] -= 10
    adjusted["clarity"] -= 6

  if not contains_constraints(prompt):
    adjusted["specificity"] -= 9
    adjusted["structure"] -= 6

  if not mentions_output_format(prompt):
    adjusted["structure"] -= 10

  return {key: clamp_score(value) for key, value in adjusted.items()}


def build_mock_response(prompt: str) -> EvaluationResponse:
  scores = {
    "clarity": 78,
    "context": 73,
    "specificity": 74,
    "structure": 79,
    "tone": 80
  }
  adjusted = apply_rule_adjustments(prompt, scores)
  overall = round(sum(adjusted.values()) / len(adjusted))
  return EvaluationResponse(
    overall_score=overall,
    scores=ScoreBreakdown(**adjusted),
    strengths=[
      "The prompt has a clear objective.",
      "Tone is suitable for professional communication."
    ],
    weaknesses=[
      "It could include more context and constraints.",
      "Expected output format is not explicit."
    ],
    suggestions=[
      "Add who the answer is for and where it will be used.",
      "Mention exact output format and desired structure.",
      "Include constraints like length, style, and must-have points."
    ],
    improved_prompt=(
      f"You are an expert assistant. Task: {prompt}\n\n"
      "Please respond using the following structure:\n"
      "1) Direct answer\n2) Key assumptions\n3) Actionable steps\n4) Final checklist\n\n"
      "Constraints: Keep the tone professional, be concise, and stay within 250 words."
    )
  )


def call_openai_for_evaluation(prompt: str) -> Dict:
  if not client:
    raise RuntimeError("OPENAI_API_KEY not configured")

  system_instruction = (
    "You are a prompt engineering evaluator. Analyze user prompts and return JSON only. "
    "Scores must be integers between 0 and 100."
  )

  user_instruction = f"""
Evaluate this user prompt for quality:
\"\"\"{prompt}\"\"\"

Return valid JSON in this exact shape:
{{
  "scores": {{
    "clarity": 0,
    "context": 0,
    "specificity": 0,
    "structure": 0,
    "tone": 0
  }},
  "strengths": ["..."],
  "weaknesses": ["..."],
  "suggestions": ["..."],
  "improved_prompt": "..."
}}
"""

  completion = client.chat.completions.create(
    model=OPENAI_MODEL,
    temperature=0.2,
    response_format={"type": "json_object"},
    messages=[
      {"role": "system", "content": system_instruction},
      {"role": "user", "content": user_instruction}
    ]
  )

  content = completion.choices[0].message.content
  if not content:
    raise RuntimeError("Model returned empty response")

  return json.loads(content)


@app.get("/health")
def health_check() -> Dict[str, str]:
  return {"status": "ok"}


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_prompt(payload: PromptRequest) -> EvaluationResponse:
  prompt = payload.prompt.strip()
  if len(prompt) < 5:
    raise HTTPException(status_code=400, detail="Prompt is too short.")

  try:
    model_output = call_openai_for_evaluation(prompt)
    base_scores = {
      "clarity": int(model_output["scores"]["clarity"]),
      "context": int(model_output["scores"]["context"]),
      "specificity": int(model_output["scores"]["specificity"]),
      "structure": int(model_output["scores"]["structure"]),
      "tone": int(model_output["scores"]["tone"])
    }
    adjusted_scores = apply_rule_adjustments(prompt, base_scores)
    overall_score = round(sum(adjusted_scores.values()) / len(adjusted_scores))

    return EvaluationResponse(
      overall_score=overall_score,
      scores=ScoreBreakdown(**adjusted_scores),
      strengths=model_output.get("strengths", [])[:5],
      weaknesses=model_output.get("weaknesses", [])[:5],
      suggestions=model_output.get("suggestions", [])[:5],
      improved_prompt=model_output.get("improved_prompt", "")
    )
  except Exception:
    return build_mock_response(prompt)
