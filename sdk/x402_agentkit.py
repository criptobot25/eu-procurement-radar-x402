"""Coinbase AgentKit Action Provider for Multi-Feed x402 Data Oracle.

Allows autonomous agents built with Coinbase AgentKit or LangChain to
consume pay-per-query intelligence feeds with automatic Base L2 USDC micropayments.
"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional
import httpx
from pydantic import BaseModel, Field

GATEWAY_URL = "https://inside-petite-legacy-reduces.trycloudflare.com"
CHAIN_ID = 8453
USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
PAYOUT_WALLET = "0xc0631209FB3d3B718d8842BC987320e6CBF7F664"


class WebExtractSchema(BaseModel):
    url: str = Field(description="Target web page URL to convert into clean, LLM-optimized Markdown")


class CryptoMarketSchema(BaseModel):
    symbol: str = Field(default="BTC", description="Crypto asset symbol (e.g., BTC, ETH, SOL)")


class WebSearchSchema(BaseModel):
    query: str = Field(description="Search query string to search the web")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of search results to return")


class BountiesFeedSchema(BaseModel):
    min_reward_usd: float = Field(default=50.0, description="Minimum bounty reward in USD/USDC")
    limit: int = Field(default=20, description="Maximum number of bounties to return")


class X402DataOracleActionProvider:
    """Coinbase AgentKit Action Provider for x402 Micro-API Marketplace."""

    name = "x402_data_oracle"

    def __init__(self, gateway_url: str = GATEWAY_URL, wallet_provider: Any = None):
        self.gateway_url = gateway_url.rstrip("/")
        self.wallet_provider = wallet_provider

    def _execute_with_x402(self, endpoint: str, payload: dict) -> dict:
        """Call endpoint, obtain HTTP 402 challenge, sign/settle via Base USDC, and return data."""
        url = f"{self.gateway_url}{endpoint}"
        with httpx.Client(timeout=15.0) as client:
            # 1. Initial invocation (returns 402 challenge)
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                return resp.json()

            if resp.status_code != 402:
                raise RuntimeError(f"Unexpected response from oracle: {resp.status_code} - {resp.text}")

            challenge_header = resp.headers.get("X-Payment-Challenge")
            detail = resp.json().get("detail", {})

            # If wallet provider is configured, sign EIP-712 or execute standard TransferWithAuthorization
            if self.wallet_provider:
                # AgentKit automatic wallet transfer / signature
                transfer_tx = self.wallet_provider.transfer(
                    to=detail.get("payment_address", PAYOUT_WALLET),
                    amount=detail.get("amount_units", "20000"),
                    asset_id=USDC_ADDRESS,
                )
                headers = {
                    "X-Payment-Challenge": challenge_header,
                    "X-Payment-Tx": transfer_tx,
                }
                final_resp = client.post(url, json=payload, headers=headers)
                final_resp.raise_for_status()
                return final_resp.json()

            # Return raw challenge info for external signing
            return {
                "status": "payment_required",
                "challenge_id": challenge_header,
                "amount_usdc": detail.get("amount_usdc", 0.02),
                "pay_to": detail.get("payment_address", PAYOUT_WALLET),
                "typed_data": detail.get("typed_data"),
            }

    def extract_web_markdown(self, args: WebExtractSchema) -> str:
        """Convert any web page into clean, ad-free Markdown for context windows."""
        result = self._execute_with_x402("/api/v1/x402/web/extract", args.model_dump())
        return json.dumps(result)

    def get_crypto_market(self, args: CryptoMarketSchema) -> str:
        """Get real-time spot price, 24h stats and perpetual funding rates."""
        result = self._execute_with_x402("/api/v1/x402/crypto/market", args.model_dump())
        return json.dumps(result)

    def search_web(self, args: WebSearchSchema) -> str:
        """Execute web search and return structured JSON results."""
        result = self._execute_with_x402("/api/v1/x402/web/search", args.model_dump())
        return json.dumps(result)

    def get_bounties_feed(self, args: BountiesFeedSchema) -> str:
        """Retrieve active software bounties paying in liquid USD/USDC."""
        result = self._execute_with_x402("/api/v1/x402/bounties/feed", args.model_dump())
        return json.dumps(result)
