import json
import logging
from openai import OpenAI, APITimeoutError, APIConnectionError, APIStatusError
from app.config import settings

logger = logging.getLogger(__name__)


def get_client() -> OpenAI:
    """
    Creates a fresh OpenAI client per request.
    No global state. Timeout set. Retries configured.
    """
    return OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        timeout=15.0,      # don't hang forever
        max_retries=2,     # retry on transient failures
        default_headers={
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }
    )


SYSTEM_INSTRUCTION = (
    "You are a prompt engineering evaluator. "
    "Analyze user prompts and return JSON only. "
    "Scores must be integers between 0 and 100. "
    "Never include markdown, backticks, or extra explanation."
)

USER_INSTRUCTION_TEMPLATE = """
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

Rules:
- strengths: max 3 items, each under 100 characters
- weaknesses: max 3 items, each under 100 characters
- suggestions: max 3 items, each under 150 characters
- improved_prompt: max 500 characters
"""


def parse_model_output(raw: str) -> dict:
    """
    Safely parses JSON from model response.
    Strips markdown fences if model misbehaves.
    """
    cleaned = raw.strip()

    # Strip ```json ... ``` if model ignores instructions
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    parsed = json.loads(cleaned)

    # Validate expected keys exist
    required_keys = {"scores", "strengths", "weaknesses", "suggestions", "improved_prompt"}
    missing = required_keys - parsed.keys()
    if missing:
        raise ValueError(f"Model response missing keys: {missing}")

    return parsed


def call_model(prompt: str) -> dict:
    """
    Calls OpenRouter API and returns parsed dict.

    Raises:
        APITimeoutError     — request took too long
        APIConnectionError  — network issue
        APIStatusError      — 4xx/5xx from OpenRouter
        ValueError          — bad JSON or missing keys
    """
    client = get_client()

    logger.info("Calling OpenRouter | model=%s | prompt_length=%d", settings.openai_model, len(prompt))

    completion = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user",   "content": USER_INSTRUCTION_TEMPLATE.format(prompt=prompt)}
        ]
    )

    raw = completion.choices[0].message.content
    if not raw:
        raise ValueError("Model returned empty response")

    logger.info("OpenRouter response received | length=%d", len(raw))

    return parse_model_output(raw)