import logging
from fastapi import Header, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# Rate Limiter
# Uses client IP address as the key.
# ─────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


async def verify_api_key(x_api_key: str = Header(...)) -> None:
    """
    Checks that every request carries the correct API key
    in the X-API-Key header.

    Frontend must send:
        headers: { "X-API-Key": "your-secret-key" }

    Raises:
        401 — missing or wrong key
    """
    if x_api_key != settings.api_secret_key:
        logger.warning("Unauthorized request — invalid API key received")
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )