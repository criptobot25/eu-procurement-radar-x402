#!/usr/bin/env python3
"""
Multi-Feed x402 Agent Client (Base L2 USDC Micropayments)

Demonstrates how autonomous AI agents query live data feeds:
- Crypto spot price & perpetual funding rates
- SSRF-safe Web to clean Markdown extraction
- Web search JSON
- Open developer bounties (USDC/USD)
- EU public procurement tenders
"""

import json
import httpx

GATEWAY_BASE_URL = "https://inside-petite-legacy-reduces.trycloudflare.com"

def run_discovery():
    print(f"[*] Discovering x402 endpoints at {GATEWAY_BASE_URL}...")
    with httpx.Client(timeout=10.0) as client:
        resp = client.get(f"{GATEWAY_BASE_URL}/.well-known/x402.json")
        resp.raise_for_status()
        manifest = resp.json()
        print(f"[+] Protocol: {manifest.get('protocol')}")
        print(f"[+] Network: {manifest.get('networkName')} (Chain ID: {manifest.get('chainId')})")
        print(f"[+] Token: {manifest.get('token', {}).get('symbol')} ({manifest.get('token', {}).get('address')})")
        print(f"[+] Pay-To Recipient: {manifest.get('payTo')}")
        print(f"[+] Price Per Query: {manifest.get('price', {}).get('amount')} USDC")
        print("[+] Registered Endpoints:")
        for ep in manifest.get("endpoints", []):
            print(f"    - {ep.get('method')} {ep.get('path')}")
        return manifest

def query_crypto_feed(symbol="BTC"):
    print(f"\n[*] Querying Crypto Market Feed for '{symbol}'...")
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(
            f"{GATEWAY_BASE_URL}/api/v1/x402/crypto/market",
            json={"symbol": symbol}
        )
        if resp.status_code == 402:
            challenge = resp.json().get("detail", {})
            print("[+] HTTP 402 Payment Challenge received:")
            print(f"    Challenge ID: {challenge.get('challenge_id')}")
            print(f"    Recipient: {challenge.get('payment_address')}")
            print(f"    Amount Units: {challenge.get('amount_units')} ({challenge.get('amount_usdc')} USDC)")
            print(f"    Resource: {challenge.get('resource')}")
            print("[+] EIP-712 Typed Data ready for agent signing.")

def query_web_extract(url="https://news.ycombinator.com"):
    print(f"\n[*] Requesting clean Markdown extraction for '{url}'...")
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(
            f"{GATEWAY_BASE_URL}/api/v1/x402/web/extract",
            json={"url": url}
        )
        if resp.status_code == 402:
            challenge = resp.json().get("detail", {})
            print("[+] HTTP 402 Payment Challenge received for Web Extractor.")
            print(f"    Challenge ID: {challenge.get('challenge_id')}")

if __name__ == "__main__":
    run_discovery()
    query_crypto_feed("BTC")
    query_web_extract("https://news.ycombinator.com")
