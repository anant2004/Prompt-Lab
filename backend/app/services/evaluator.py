import logging
from openai import APITimeoutError, APIConnectionError, APIStatusError

from app.utils.scoring import apply_rule_adjustments, compute_overall
from app.utils.validators import validate_prompt
from app.services.openrouter import call_model
from app.models.schemas import EvaluationResponse, ScoreBreakdown

logger = logging.getLogger(__name__)


def build_fallback_response(prompt: str) -> EvaluationResponse:
    """
    Returns a rule-based response when AI call fails.
    Honest about being a fallback — scores reflect
    only what rules can detect, not AI analysis.
    """
    base_scores = {
        "clarity":     70,
        "context":     70,
        "specificity": 70,
        "structure":   70,
        "tone":        70,
    }
    adjusted = apply_rule_adjustments(prompt, base_scores)
    overall = compute_overall(adjusted)

    logger.warning("Returning fallback response | overall=%d", overall)

    return EvaluationResponse(
        overall_score=overall,
        scores=ScoreBreakdown(**adjusted),
        strengths=[
            "Unable to perform full AI analysis.",
            "Scores reflect rule-based evaluation only."
        ],
        weaknesses=[
            "AI service was unavailable for deep analysis."
        ],
        suggestions=[
            "Try again in a moment for full AI-powered feedback.",
            "Ensure your prompt has clear constraints and output format.",
            "Aim for 20-100 words for best results."
        ],
        improved_prompt=(
            "AI service unavailable. "
            "Please retry for an improved prompt suggestion."
        )
    )


def run_evaluation(prompt: str) -> tuple[EvaluationResponse, bool]:
    """
    Master evaluation pipeline.

    Steps:
        1. Validate input
        2. Call AI for scores
        3. Apply rule adjustments on top
        4. Return final response

    Returns:
        (EvaluationResponse, is_ai_powered: bool)
        is_ai_powered=False means fallback was used.

    Raises:
        ValueError — if prompt fails validation
    """

    # Step 1 — Validate
    is_valid, error = validate_prompt(prompt)
    if not is_valid:
        raise ValueError(error)

    # Step 2 — Call AI
    try:
        model_output = call_model(prompt)

        # Step 3 — Extract and clamp AI scores
        raw_scores = {
            "clarity":     int(model_output["scores"]["clarity"]),
            "context":     int(model_output["scores"]["context"]),
            "specificity": int(model_output["scores"]["specificity"]),
            "structure":   int(model_output["scores"]["structure"]),
            "tone":        int(model_output["scores"]["tone"]),
        }

        # Step 4 — Apply rule adjustments on top of AI scores
        adjusted = apply_rule_adjustments(prompt, raw_scores)
        overall  = compute_overall(adjusted)

        logger.info("Evaluation complete | overall=%d | ai_powered=True", overall)

        return EvaluationResponse(
            overall_score=overall,
            scores=ScoreBreakdown(**adjusted),
            strengths=model_output.get("strengths",  [])[:3],
            weaknesses=model_output.get("weaknesses", [])[:3],
            suggestions=model_output.get("suggestions",[])[:3],
            improved_prompt=model_output.get("improved_prompt", "")[:2000]
        ), True

    except (APITimeoutError, APIConnectionError) as e:
        logger.error("Network error calling OpenRouter: %s", str(e))
        return build_fallback_response(prompt), False

    except APIStatusError as e:
        logger.error("OpenRouter API error | status=%d | %s", e.status_code, str(e))
        return build_fallback_response(prompt), False

    except (ValueError, KeyError) as e:
        logger.error("Bad model output: %s", str(e))
        return build_fallback_response(prompt), False
    
    except Exception as e:                               
        logger.error("Unexpected error during evaluation: %s", str(e))
        return build_fallback_response(prompt), False