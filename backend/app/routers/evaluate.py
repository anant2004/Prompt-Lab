import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi.errors import RateLimitExceeded

from app.models.schemas import PromptRequest, EvaluationResponse
from app.services.evaluator import run_evaluation
from app.dependencies import limiter, verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["evaluate"])


@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    summary="Evaluate a prompt for quality"
)
@limiter.limit("10/minute")
async def evaluate_prompt(
    request: Request,
    payload: PromptRequest,
    _: None = Depends(verify_api_key),
) -> EvaluationResponse:
    """
    Evaluates a prompt across 5 dimensions:
    clarity, context, specificity, structure, tone.

    Headers required:
        X-API-Key: your-secret-key

    Rate limit:
        10 requests per minute per IP
    """
    try:
        response, is_ai_powered = run_evaluation(payload.prompt)

        if not is_ai_powered:
            logger.warning("Fallback used for request | prompt_length=%d",
                           len(payload.prompt))

        return response

    except ValueError as e:
        # Validation failure from run_evaluation
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Anything unexpected — log full traceback
        logger.exception("Unhandled error in /evaluate: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")