import re
from typing import Dict

PENALTIES = {
    "too_short_clarity":      {"points": 12, "reason": "Under 10 words — clarity suffers"},
    "too_short_context":      {"points": 14, "reason": "Under 10 words — no context given"},
    "too_short_specificity":  {"points": 14, "reason": "Under 10 words — too vague"},
    "too_long_structure":     {"points": 8,  "reason": "Over 180 words — structure gets bloated"},
    "vague_words_specificity":{"points": 10, "reason": "3+ vague words hurt specificity"},
    "vague_words_clarity":    {"points": 6,  "reason": "3+ vague words hurt clarity"},
    "no_constraints_spec":    {"points": 9,  "reason": "No constraint words found"},
    "no_constraints_struct":  {"points": 6,  "reason": "No constraint words found"},
    "no_format_structure":    {"points": 10, "reason": "No output format mentioned"},
}

VAGUE_WORDS = [
    "good", "nice", "better", "optimize",
    "improve", "something", "stuff", "best"
]

CONSTRAINT_PATTERNS = [
    r"\bmax\b", r"\bmin\b", r"\bwithin\b",
    r"\blimit\b", r"\bexactly\b", r"\bmust\b"
]

FORMAT_PATTERNS = [
    r"\bjson\b", r"\btable\b", r"\bbullet",
    r"\bmarkdown\b", r"\bformat\b", r"\bsections?\b"
]

def clamp(value: int) -> int:
    return max(0, min(100, value))

def count_vague_words(prompt: str) -> int:
    lowered = prompt.lower()
    return sum(lowered.count(word) for word in VAGUE_WORDS)

def has_constraints(prompt: str) -> bool:
    return any(
        re.search(pattern, prompt, re.IGNORECASE)
        for pattern in CONSTRAINT_PATTERNS
    )

def has_output_format(prompt: str) -> bool:
    return any(
        re.search(pattern, prompt, re.IGNORECASE)
        for pattern in FORMAT_PATTERNS
    )

def apply_rule_adjustments(prompt: str, scores: Dict[str, int]) -> Dict[str, int]:
    adjusted = scores.copy()
    word_count = len(prompt.split())

    # Penalty: prompt too short
    if word_count < 10:
        adjusted["clarity"]     -= PENALTIES["too_short_clarity"]["points"]
        adjusted["context"]     -= PENALTIES["too_short_context"]["points"]
        adjusted["specificity"] -= PENALTIES["too_short_specificity"]["points"]

    # Penalty: prompt too long
    if word_count > 180:
        adjusted["structure"] -= PENALTIES["too_long_structure"]["points"]

    # Penalty: vague language
    if count_vague_words(prompt) >= 3:
        adjusted["specificity"] -= PENALTIES["vague_words_specificity"]["points"]
        adjusted["clarity"]     -= PENALTIES["vague_words_clarity"]["points"]

    # Penalty: no constraints mentioned
    if not has_constraints(prompt):
        adjusted["specificity"] -= PENALTIES["no_constraints_spec"]["points"]
        adjusted["structure"]   -= PENALTIES["no_constraints_struct"]["points"]

    # Penalty: no output format mentioned
    if not has_output_format(prompt):
        adjusted["structure"] -= PENALTIES["no_format_structure"]["points"]

    # Clamp all scores to 0–100
    return {key: clamp(value) for key, value in adjusted.items()}

def compute_overall(scores: Dict[str, int]) -> int:
    return round(sum(scores.values()) / len(scores))

