import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?instructions",
    r"forget\s+(all\s+)?previous",
    r"you\s+are\s+now",
    r"act\s+as\s+(a\s+)?(?!professional|expert|senior)",  # blocks "act as a hacker" not "act as an expert"
    r"jailbreak",
    r"pretend\s+you",
    r"disregard\s+(all\s+)?",
]


def is_injection_attempt(prompt: str) -> bool:
    """
    Checks if the prompt is trying to manipulate
    the AI evaluator through instruction hijacking.
    """
    lowered = prompt.lower()
    return any(
        re.search(pattern, lowered)
        for pattern in INJECTION_PATTERNS
    )


def is_mostly_code(prompt: str) -> bool:
    """
    Detects if someone submitted raw code instead
    of a prompt. Code is not a prompt — reject it.
    """
    code_indicators = [
        r"def\s+\w+\s*\(",       # Python function
        r"import\s+\w+",          # import statement
        r"class\s+\w+\s*[\(:]",   # class definition
        r"#include\s*<",          # C/C++
        r"public\s+static\s+void",# Java
        r"<\?php",                # PHP
    ]
    matches = sum(
        1 for pattern in code_indicators
        if re.search(pattern, prompt)
    )
    return matches >= 2  # 2+ indicators = likely code


def sanitize_text(text: str) -> str:
    """
    Strips control characters from any string.
    Use on prompt input before processing.
    """
    return re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text).strip()


def validate_prompt(prompt: str) -> tuple[bool, str]:
    """
    Master validator. Returns (is_valid, error_message).
    Empty error message means valid.

    Usage:
        valid, error = validate_prompt(prompt)
        if not valid:
            raise HTTPException(400, detail=error)
    """
    prompt = sanitize_text(prompt)

    if len(prompt.split()) < 3:
        return False, "Prompt is too short to evaluate meaningfully."

    if is_injection_attempt(prompt):
        return False, "Prompt contains invalid patterns."

    if is_mostly_code(prompt):
        return False, "Please submit a prompt, not a code snippet."

    return True, ""