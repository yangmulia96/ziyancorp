// Shared constants untuk /api/proxy dan /api/models.
// Vercel tidak support auto-import antar function, jadi duplikasi (DRY) di sini.

export const ENDPOINTS = {
  xkiro: "https://api.xkiro.com/v1/chat/completions",
  openrouter: "https://openrouter.ai/api/v1/chat/completions",
};

export const DEFAULT_MODELS = {
  xkiro: "qwen/qwen3.8-max:free",
  openrouter: "google/gemini-2.5-flash",
};

export const ALLOWED_MODELS = {
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
