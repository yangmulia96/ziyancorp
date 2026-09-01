---
name: 9router-free-models
description: Identify free-tier models in 9Router for zero-cost LLM use.
---

# 9Router Free Model Identification

## When to Use
User asks about free models in 9Router, needs zero-cost LLM options, or requests model filtering by cost.

## Discovery Commands
```bash
# List all models
curl -s http://localhost:20128/v1/models

# Filter free models (42 of 77 total)
curl -s http://localhost:20128/v1/models | python3 -c "
import sys,json
d=json.load(sys.stdin)
free=[m for m in d['data'] if ':free' in m['id'] or m['owned_by'] in ['cf','kgw','kr','combo']]
print(f'Free: {len(free)}')
for f in free: print(f'  {f[\"id\"]} ({f[\"owned_by\"]})')"
```

## Free Model Categories
- **KR Free** (7): kr/auto, thinking, agentic variants
- **CF Free Tier** (12): Llama, Mistral, DeepSeek, Qwen
- **KGW Free** (4): kilo-auto tiers
- **COMBO** (1): gratis-banyak
- **OPRU Free** (6): openrouter/*:free
- **GEMINI** (2): gemini-3.6-flash, gemini-3.5-flash-lite

## ZIYAN Pipeline Recommendations
- YouTube Shorts: gemini/gemini-3.6-flash (1M ctx, vision+search)
- Affiliate: kr/auto or gratis-banyak
- Microstock: cf/@cf/moonshotai/kimi-k2.5 (vision+reasoning)
- Telegram SaaS: kgw/kilo-auto/free

## Pitfalls
1. Free models have rate limits
2. Context windows vary (128k-1M tokens)
3. Capability trade-offs vs paid
4. Models can be removed without notice
5. Use json.JSONDecoder().raw_decode for 9Router JSON (trailing text)