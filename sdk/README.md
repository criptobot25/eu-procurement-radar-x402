# 🌐 x402 Multi-Feed Data Oracle for Autonomous AI Agents

> **Pay-per-query intelligence feeds on Base L2 USDC ($0.02 / query)**  
> Built for autonomous agents (Coinbase AgentKit, ElizaOS, LangChain, AutoGen).

---

## ⚡ Live Discovery Endpoints

- **Gateway URL:** `https://inside-petite-legacy-reduces.trycloudflare.com`
- **x402 Protocol Manifest:** `https://inside-petite-legacy-reduces.trycloudflare.com/.well-known/x402.json`
- **Agent Capabilities Manifest:** `https://inside-petite-legacy-reduces.trycloudflare.com/.well-known/ai-agent.json`
- **Network:** Base L2 (Chain ID `8453`)
- **Asset:** Circle USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- **Payment Address:** `0xc0631209FB3d3B718d8842BC987320e6CBF7F664`

---

## 🛠️ Available Micro-API Feeds

| Endpoint | Method | Cost | Description |
|---|---|---|---|
| `/api/v1/x402/web/extract` | POST | $0.02 USDC | SSRF-hardened HTML-to-Markdown extraction for LLM context windows |
| `/api/v1/x402/crypto/market` | POST | $0.02 USDC | Real-time spot price + perpetual funding rate feeds |
| `/api/v1/x402/web/search` | POST | $0.02 USDC | Clean structured JSON web search results |
| `/api/v1/x402/bounties/feed` | POST | $0.02 USDC | Filtered liquid GitHub bounties feed ($50+) |
| `/api/v1/x402/query` | POST | $0.02 USDC | EU Public Procurement Tenders (TED v3) database |

---

## 🤖 1. Python SDK — Coinbase AgentKit & LangChain

```python
from x402_agentkit import X402DataOracleActionProvider, WebExtractSchema, CryptoMarketSchema

# Initialize action provider
oracle = X402DataOracleActionProvider(
    gateway_url="https://inside-petite-legacy-reduces.trycloudflare.com",
    wallet_provider=agent_wallet  # Any AgentKit WalletProvider
)

# 1. Extract clean web Markdown
markdown_data = oracle.extract_web_markdown(
    WebExtractSchema(url="https://news.ycombinator.com")
)

# 2. Get Bitcoin spot price & perpetual funding rate
crypto_data = oracle.get_crypto_market(
    CryptoMarketSchema(symbol="BTC")
)
```

---

## 👾 2. TypeScript SDK — ElizaOS Plugin

```typescript
import { x402OraclePlugin } from "@antigravity/x402-oracle";

// Register inside ElizaOS character runtime
const agentRuntime = new AgentRuntime({
  plugins: [x402OraclePlugin],
  // ...
});
```

When an agent needs real-time market data or web scraping, it seamlessly queries the Oracle and pays $0.02 USDC via its Base wallet.
