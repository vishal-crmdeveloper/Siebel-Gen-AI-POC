"""
LLM service layer — abstracts away the provider so the API
routes never care whether we're hitting Ollama, OpenAI, or Anthropic.
"""

from __future__ import annotations

import json
import logging
import traceback

import httpx

from app.config import settings
from app.models import OrderSummaryRequest

logger = logging.getLogger(__name__)


# ── Prompt Builder ──────────────────────────────────────────


def _build_prompt(order: OrderSummaryRequest) -> str:
    """
    Convert an order payload into a clear prompt for any LLM.
    If the user provided a specific question, tailor the prompt to answer it.
    """
    items_text = "\n".join(
        f"  - {item.product_name}: Qty {item.quantity} × ${item.unit_price:,.2f} = ${item.total_price:,.2f}"
        + (f" (Discount: ${item.discount:,.2f})" if item.discount else "")
        for item in order.line_items
    )

    # Build instruction based on whether user asked a specific question
    if order.user_question and order.user_question.strip():
        instruction = f"""You are an AI assistant integrated with Oracle Siebel CRM.
A user has asked the following question about an order:

USER QUESTION: {order.user_question.strip()}

Analyze the order details below and provide a clear, professional answer
to the user's question."""
    else:
        instruction = """You are an AI assistant integrated with Oracle Siebel CRM.
Analyze the following order and provide a concise, professional summary
that a sales representative or manager can quickly review.

Include:
1. A brief overview of the order
2. Key details (customer, date, status, total value)
3. Line item highlights
4. Any notable observations or recommendations"""

    prompt = f"""{instruction}

ORDER DETAILS:
───────────────────────────────
Order ID      : {order.order_id}
Customer      : {order.customer_name}
Order Date    : {order.order_date}
Status        : {order.status}
Priority      : {order.priority or "Normal"}
Currency      : {order.currency}
Total Amount  : ${order.total_amount:,.2f}

Line Items:
{items_text}

Notes         : {order.notes or "None"}
Shipping Addr : {order.shipping_address or "Not specified"}
───────────────────────────────

Provide your response in a clear, professional format."""

    return prompt


# ── Provider Implementations ───────────────────────────────


async def _call_ollama(prompt: str) -> tuple[str, str]:
    """Call a local Ollama instance. Returns (response_text, model_name)."""
    model = settings.OLLAMA_MODEL
    url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=30.0)) as client:
        logger.info(f"Calling Ollama at {url} with model {model}")
        response = await client.post(
            url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()

    return data.get("response", ""), model


async def _call_openai(prompt: str) -> tuple[str, str]:
    """Call OpenAI Chat Completions API. Returns (response_text, model_name)."""
    model = settings.OPENAI_MODEL
    url = "https://api.openai.com/v1/chat/completions"

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful CRM assistant that summarizes Siebel orders."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"], model


async def _call_anthropic(prompt: str) -> tuple[str, str]:
    """Call Anthropic Messages API. Returns (response_text, model_name)."""
    model = settings.ANTHROPIC_MODEL
    url = "https://api.anthropic.com/v1/messages"

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": prompt},
                ],
                "system": "You are a helpful CRM assistant that summarizes Siebel orders.",
                "temperature": 0.3,
            },
        )
        response.raise_for_status()
        data = response.json()

    return data["content"][0]["text"], model


# ── Public Interface ────────────────────────────────────────

_PROVIDERS = {
    "ollama": _call_ollama,
    "openai": _call_openai,
    "anthropic": _call_anthropic,
}


async def summarize_order(order: OrderSummaryRequest) -> tuple[str, str, str]:
    """
    Generate an AI summary for the given order.

    Returns:
        (summary_text, provider_name, model_name)
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider not in _PROVIDERS:
        raise ValueError(
            f"Unknown LLM_PROVIDER '{provider}'. "
            f"Supported: {', '.join(_PROVIDERS.keys())}"
        )

    prompt = _build_prompt(order)
    call_fn = _PROVIDERS[provider]
    response_text, model_name = await call_fn(prompt)

    return response_text, provider, model_name
