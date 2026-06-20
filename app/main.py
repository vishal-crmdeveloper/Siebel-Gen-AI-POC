"""
FastAPI application — Siebel Order Summarization API.
"""

from __future__ import annotations

import logging
import traceback
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.models import (
    HealthResponse,
    OrderSummaryRequest,
    OrderSummaryResponse,
)
from app.llm_service import summarize_order

logger = logging.getLogger(__name__)


# ── Application ─────────────────────────────────────────────

app = FastAPI(
    title="Siebel Order Summarization API",
    description=(
        "A Gen AI POC that integrates Oracle Siebel CRM with Large Language Models. "
        "Send order details and receive an AI-generated summary."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow Siebel / any front-end to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve the static UI
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Routes ──────────────────────────────────────────────────


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to the UI dashboard."""
    return RedirectResponse(url="/static/index.html")


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check if the API and LLM provider are configured."""
    return HealthResponse(
        status="healthy",
        provider=settings.LLM_PROVIDER,
        model=getattr(
            settings,
            f"{settings.LLM_PROVIDER.upper()}_MODEL",
            "unknown",
        ),
    )


@app.post(
    "/api/v1/summarize-order",
    response_model=OrderSummaryResponse,
    tags=["Orders"],
    summary="Summarize a Siebel order",
    description="Accepts order details from Oracle Siebel and returns an AI-generated summary.",
)
async def summarize_order_endpoint(order: OrderSummaryRequest):
    """
    Receive order details and return an AI summary.

    The LLM provider is determined by the `LLM_PROVIDER` environment variable.
    """
    try:
        summary_text, provider, model = await summarize_order(order)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        error_type = type(exc).__name__
        error_msg = str(exc) or "No details available"
        logger.error(f"LLM call failed ({error_type}): {error_msg}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=502,
            detail=f"LLM call failed ({error_type}): {error_msg}",
        )

    return OrderSummaryResponse(
        order_id=order.order_id,
        summary=summary_text,
        provider=provider,
        model=model,
    )


# ── Entrypoint (optional: python app/main.py) ──────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
