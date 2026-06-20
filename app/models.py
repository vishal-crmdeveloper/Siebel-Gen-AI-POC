"""
Pydantic models for API request / response schemas.
Mirrors typical Oracle Siebel order structure.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


# ── Request Models ──────────────────────────────────────────


class OrderLineItem(BaseModel):
    """A single line item within an order."""

    product_name: str = Field(..., description="Product or service name")
    quantity: int = Field(..., ge=1, description="Quantity ordered")
    unit_price: float = Field(..., ge=0, description="Price per unit")
    total_price: float = Field(..., ge=0, description="Line total")
    product_id: Optional[str] = Field(None, description="Siebel product row ID")
    discount: Optional[float] = Field(None, ge=0, description="Discount amount")


class OrderSummaryRequest(BaseModel):
    """
    Payload representing an Oracle Siebel order.
    Send this to /api/v1/summarize-order to get an AI summary.
    """

    order_id: str = Field(..., description="Siebel order number / row ID")
    customer_name: str = Field(..., description="Account or contact name")
    order_date: str = Field(..., description="Order creation date (YYYY-MM-DD)")
    status: str = Field(..., description="Order status (e.g. Open, In Progress, Complete)")
    line_items: list[OrderLineItem] = Field(
        ..., min_length=1, description="At least one line item"
    )
    total_amount: float = Field(..., ge=0, description="Order total value")
    currency: str = Field("USD", description="Currency code")
    notes: Optional[str] = Field(None, description="Additional notes or comments")
    priority: Optional[str] = Field(None, description="Order priority level")
    shipping_address: Optional[str] = Field(None, description="Delivery address")
    user_question: Optional[str] = Field(
        None,
        description="Optional specific question about the order (e.g. 'What risks do you see?')",
    )


# ── Response Models ─────────────────────────────────────────


class OrderSummaryResponse(BaseModel):
    """Returned by the summarize-order endpoint."""

    order_id: str
    summary: str = Field(..., description="AI-generated order summary")
    provider: str = Field(..., description="LLM provider used (ollama/openai/anthropic)")
    model: str = Field(..., description="Model name used for generation")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    provider: str
    model: str
