// Vercel serverless function: /api/proxy
// Bypass CORS untuk xKiro / OpenRouter dari browser PWA.
// Ini Node.js native, jadi Vercel execute langsung tanpa runtime custom.

const ENDPOINTS = {
  xkiro: "https://api.xkiro.com/v1/chat/completions",
  openrouter: "https://openrouter.ai/api/v1/chat/completions",
};

const DEFAULT_MODELS = {
  xkiro: "qwen/qwen3.8-max:free",
  openrouter: "google/gemini-2.5-flash",
};

const DEFAULT_KEYS = {
  xkiro: process.env.XKIRO_API_KEY || "",
  openrouter: process.env.OPENROUTER_API_KEY || ""
};

const ALLOWED_MODELS = {
  xkiro: [
    "qwen/qwen3.7-max:free",
    "qwen/qwen3.8-max:free",
    "qwen/qwen3.6-max-preview:free",
    "qwen/qwen3.5-flash:free",
    "qwen/qwen3.5-omni-flash:free",
    "qwen/qwen3-coder-plus:free",
    "minimax/minimax-m3:free",
    "minimax/minimax-m2.5:free",
    "minimax/minimax-m2.7-highspeed:free",
  ],
  openrouter: [
    "google/gemini-2.5-flash",
    "google/gemini-2.5-flash-lite",
    "meta/llama-3.3-70b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "deepseek/deepseek-chat-v3.1:free",
  ],
};

export default async function handler(req, res) {
  // CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS, GET");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method === "GET") {
    return res.status(200).json({
      info: "POST to this endpoint with { provider, apiKey, model, messages, responseFormat? }",
      providers: Object.keys(ENDPOINTS),
      defaults: DEFAULT_MODELS,
      models: ALLOWED_MODELS,
    });
  }
  if (req.method !== "POST") return res.status(405).json({ error: "method_not_allowed" });

  try {
    const { provider, apiKey, model, messages, responseFormat } = req.body || {};
    if (!provider || !ENDPOINTS[provider]) {
      return res.status(400).json({ error: "invalid_provider", allowed: Object.keys(ENDPOINTS) });
    }
    const activeKey = apiKey || DEFAULT_KEYS[provider];
    if (!activeKey) return res.status(400).json({ error: "missing_api_key" });
    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: "missing_messages" });
    }

    const useModel = ALLOWED_MODELS[provider].includes(model) ? model : DEFAULT_MODELS[provider];

    const body = { model: useModel, messages, temperature: 0.85 };
    if (responseFormat) body.response_format = responseFormat;

    const upstream = await fetch(ENDPOINTS[provider], {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${activeKey}`,
        "User-Agent": "NarasiKilat-PWA/1.0",
      },
      body: JSON.stringify(body),
    });

    const text = await upstream.text();
    if (!upstream.ok) {
      return res.status(upstream.status).json({
        error: "upstream_error",
        provider,
        model: useModel,
        detail: text.slice(0, 500),
      });
    }

    const data = JSON.parse(text);
    return res.status(200).json({ ...data, _meta: { provider, model: useModel } });
  } catch (e) {
    return res.status(500).json({ error: "proxy_failed", detail: String(e).slice(0, 300) });
  }
}

export const config = {
  api: { bodyParser: { sizeLimit: "1mb" } },
};
