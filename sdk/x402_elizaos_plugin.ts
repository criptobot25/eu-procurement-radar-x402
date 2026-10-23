/**
 * ElizaOS Plugin: Multi-Feed x402 Data Oracle (Base L2 USDC)
 * Enables ElizaOS agents to consume pay-per-query APIs using micropayments.
 */

export interface X402OracleConfig {
  gatewayUrl?: string;
  payoutWallet?: string;
}

export const x402OraclePlugin = {
  name: "x402-data-oracle",
  description: "Pay-per-query data feeds for web extraction, crypto market intelligence, and search with Base USDC.",
  
  actions: [
    {
      name: "EXTRACT_WEB_MARKDOWN",
      similes: ["SCRAPE_WEBPAGE", "READ_URL_AS_MARKDOWN", "CONVERT_PAGE_TO_TEXT"],
      description: "Extract clean, ad-free Markdown from any URL using the x402 Oracle.",
      examples: [
        [
          { user: "{{user1}}", content: { text: "Extract content from https://news.ycombinator.com" } },
          { user: "{{agentName}}", content: { text: "Extracting clean Markdown via x402 Oracle..." } }
        ]
      ],
      validate: async (runtime: any, message: any) => true,
      handler: async (runtime: any, message: any, state: any, options: any, callback: any) => {
        const url = options?.url || "https://news.ycombinator.com";
        const gateway = "https://inside-petite-legacy-reduces.trycloudflare.com";
        const res = await fetch(`${gateway}/api/v1/x402/web/extract`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url })
        });
        const data = await res.json();
        callback?.({ text: `Oracle Response: ${JSON.stringify(data).slice(0, 300)}...` });
        return data;
      }
    },
    {
      name: "GET_CRYPTO_MARKET_DATA",
      similes: ["CHECK_CRYPTO_PRICE", "GET_FUNDING_RATE", "CRYPTO_ORACLE"],
      description: "Retrieve verified spot price and perpetual funding rates for BTC, ETH, SOL, BASE.",
      examples: [
        [
          { user: "{{user1}}", content: { text: "What is the BTC price and perp funding rate?" } },
          { user: "{{agentName}}", content: { text: "Querying x402 Crypto Oracle on Base..." } }
        ]
      ],
      validate: async (runtime: any, message: any) => true,
      handler: async (runtime: any, message: any, state: any, options: any, callback: any) => {
        const symbol = options?.symbol || "BTC";
        const gateway = "https://inside-petite-legacy-reduces.trycloudflare.com";
        const res = await fetch(`${gateway}/api/v1/x402/crypto/market`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ symbol })
        });
        const data = await res.json();
        callback?.({ text: `Crypto Oracle Data for ${symbol}: ${JSON.stringify(data)}` });
        return data;
      }
    }
  ]
};
