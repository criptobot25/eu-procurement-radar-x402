# Multi-Feed x402 Agent Data Oracle & Micro-API Marketplace

> Autonomous, pay-per-query data feeds and web microservices for AI Agents, LLMs, and trading bots settled via HTTP 402 with Circle USDC on Base L2 (Chain ID 8453).

---

## Overview

The **Multi-Feed x402 Agent Data Oracle** solves the API subscription trap for autonomous agents. Instead of paying $250+/month per API service, AI agents pay **$0.01 to $0.02 USDC per request** with instant cryptographic micro-settlement on Base.

### Key Characteristics:
- **Zero Subscription / Zero Account Creation:** Autonomous agents invoke the API directly with their EVM wallet.
- **Settlement Network:** Base L2 (`eip155:8453`).
- **Currency:** Circle USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`).
- **Recipient Address:** `0xc0631209FB3d3B718d8842BC987320e6CBF7F664`.
- **Supported Standards:** x402 v2 (EIP-3009 TransferWithAuthorization) and EIP-712 Receipt Proofs.

---

## Live Multi-Feed Catalog

| Feed / Endpoint | Description | Pricing | Request Method |
|---|---|---|---|
| **`POST /api/v1/x402/web/extract`** | SSRF-safe Web to clean Markdown extractor (Firecrawl alternative) | $0.02 USDC | JSON `{"url": "https://..."}` |
| **`POST /api/v1/x402/crypto/market`** | Real-time Spot price, 24h stats, and Perpetual Funding Rates | $0.02 USDC | JSON `{"symbol": "BTC"}` |
| **`POST /api/v1/x402/web/search`** | Organic web search returning structured JSON without Google/Bing keys | $0.02 USDC | JSON `{"query": "...", "limit": 5}` |
| **`POST /api/v1/x402/bounties/feed`** | Filtered stream of active software bounties paying in liquid USD/USDC | $0.02 USDC | JSON `{"min_reward_usd": 50}` |
| **`POST /api/v1/x402/query`** | European Union Public Procurement Tenders (TED API v3 / CPVs) | $0.02 USDC | JSON `{"query": "cloud", "country": "DEU"}` |

---

## Discovery & Manifests

- **x402 Protocol Discovery:** `https://inside-petite-legacy-reduces.trycloudflare.com/.well-known/x402.json`
- **AI Agent Tool Manifest (OpenAPI 3.1):** `https://inside-petite-legacy-reduces.trycloudflare.com/.well-known/ai-agent.json`

---

## Quickstart for AI Agents (Python)

```python
import httpx

API_BASE = 'https://inside-petite-legacy-reduces.trycloudflare.com'

# 1. Inspect Discovery Manifest
discovery = httpx.get(f'{API_BASE}/.well-known/x402.json').json()
print('Payment Address:', discovery['payTo'])
print('Price:', discovery['price']['amount'], discovery['price']['currency'])

# 2. Query any feed - server returns HTTP 402 with signed challenge
res = httpx.post(f'{API_BASE}/api/v1/x402/crypto/market', json={'symbol': 'BTC'})
if res.status_code == 402:
    challenge = res.json()['detail']
    print('Challenge ID:', challenge['challenge_id'])
    print('EIP-712 Typed Data:', challenge['typed_data'])
    # Sign challenge typed_data with your Base wallet, then submit:
    # headers = {'X-Payment-Challenge': challenge['challenge_id'], 'X-Payment-Proof': json.dumps({'signature': sig, 'tx_hash': tx})}
```

---

## Institutional Security & Verification
- **SSRF Hardened:** Prohibits RFC 1918, RFC 3927 link-local, loopback, and cloud metadata (169.254.169.254).
- **Anti-Replay Nonce Verification:** Every payment proof is cryptographically checked and bound to the exact request SHA-256 body hash.
- **Strict Currency Filter:** Zero shitcoins / memecoins. Exclusively operates in liquid Circle USDC.
