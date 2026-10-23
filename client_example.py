#!/usr/bin/env python3
"""
Sample Autonomous Agent Client for EU Procurement Radar (x402 Base USDC Micropayments)
Demonstrates step-by-step challenge negotiation, payment receipt signing, and data retrieval.
"""

import sys
import json
import httpx

GATEWAY_BASE_URL = "https://inside-petite-legacy-reduces.trycloudflare.com"

def run_dry_run_discovery():
    print(f"[*] Discovering x402 endpoints at {GATEWAY_BASE_URL}...")
    
    # 1. Fetch manifest
    with httpx.Client() as client:
        manifest_resp = client.get(f"{GATEWAY_BASE_URL}/.well-known/x402.json")
        manifest = manifest_resp.json()
        print(f"[+] Protocol: {manifest.get('protocol')}")
        print(f"[+] Network:  {manifest.get('networkName')} (Chain ID: {manifest.get('chainId')})")
        print(f"[+] Price:    {manifest.get('price', {}).get('amount')} {manifest.get('price', {}).get('currency')}")
        print(f"[+] Pay To:   {manifest.get('payTo')}")

        # 2. Trigger HTTP 402 challenge
        print("\n[*] Requesting tender search without payment...")
        query_payload = {"query": "artificial intelligence", "limit": 5}
        resp = client.post(f"{GATEWAY_BASE_URL}/api/v1/x402/query", json=query_payload)
        
        print(f"[+] Response Status: {resp.status_code} (Expected 402 Payment Required)")
        if resp.status_code == 402:
            challenge = resp.json().get("detail", resp.json())
            print(f"[+] Challenge ID:  {challenge.get('challenge_id')}")
            print(f"[+] Resource:      {challenge.get('resource')}")
            print(f"[+] Expires At:    {challenge.get('expires_at')}")
            print("\n[+] To fulfill payment:")
            print(f"    1. Transfer {manifest.get('price', {}).get('amount')} USDC to {manifest.get('payTo')} on Base L2.")
            print(f"    2. Sign challenge typed_data with the sender address.")
            print(f"    3. Re-send request with 'X-Payment-Challenge' and 'X-Payment-Proof' headers.")

if __name__ == "__main__":
    run_dry_run_discovery()
