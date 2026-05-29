import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.dependencies import limiter
from app.routers import evaluate

# ─────────────────────────────────────────
# Logging — runs before anything else
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# App
# ─────────────────────────────────────────
app = FastAPI(
    title="Prompt Lab API",
    version="2.0.0",
    description="Evaluates AI prompts across 5 quality dimensions."
)

# ─────────────────────────────────────────
# Rate limiter
# ─────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ─────────────────────────────────────────
# CORS
# ─────────────────────────────────────────
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if settings.frontend_origin not in allowed_origins:
    allowed_origins.append(settings.frontend_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],   # only what you actually use
    allow_headers=["Content-Type", "X-API-Key"],
)

# ─────────────────────────────────────────
# Routers
# ─────────────────────────────────────────
app.include_router(evaluate.router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "version": "2.0.0"}


logger.info("Prompt Lab API started successfully")