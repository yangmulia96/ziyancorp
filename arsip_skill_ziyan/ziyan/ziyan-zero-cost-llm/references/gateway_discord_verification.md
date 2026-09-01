# Discord Gateway & 9Router Routing Verification

## Discord Gateway Token Location
**Pattern discovered**: Discord bot token may be stored in `C:\Users\arija\AppData\Local\hermes\.env` while the main `.env` in Roaming directory is empty.

### Verification steps:
```bash
# Check token location
grep -E "DISCORD_BOT_TOKEN=" "$LOCALAPPDATA/hermes/.env" 2>/dev/null | sed 's/TOKEN=.*/TOKEN=<redacted>/'
grep -E "DISCORD_BOT_TOKEN=" "$APPDATA/hermes/.env" 2>/dev/null | sed 's/TOKEN=.*/TOKEN=<redacted>/'

# Test bot connectivity
curl -s -H "Authorization: Bot $TOKEN" "https://discord.com/api/v10/users/@me" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Bot: {d.get('username','?')}#{d.get('discriminator','?')} (ID: {d.get('id','?')})\")"

# List accessible channels
curl -s -H "Authorization: Bot $TOKEN" "https://discord.com/api/v10/users/@me/guilds" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Guilds: {len(d)}\"); [print(f\"  - {g['name']} (ID: {g['id']})\") for g in d[:3]]"
```

### Hermes Gateway Status Check
```bash
# Gateway process
hermes gateway status
hermes gateway list

# Send test message
hermes send --to discord:hq "✓ Gateway verification test" 2>&1 | grep -v "GOOGLE_KEY\|Unicode"

# Check if gateway is actually using Discord (vs Telegram/WhatsApp)
```

## 9Router Channel-Researcher Combo Inspection

### SQLite Query for Active Routing
```bash
# Path to 9Router database
DB="C:/Users/arija/AppData/Roaming/9router/db/data.sqlite"

# Get channel-researcher combo configuration
sqlite3 "$DB" "SELECT name, SUBSTR(models,1,200) FROM combos WHERE name LIKE '%channel%' OR name LIKE '%researcher%'" 2>/dev/null

# Count free vs paid models in combo
sqlite3 "$DB" "
SELECT 
  name,
  COUNT(*) as total_models,
  SUM(CASE WHEN models LIKE '%:free%' OR models LIKE '%kr/%' OR models LIKE '%kgw/%' OR models LIKE '%cf/%' THEN 1 ELSE 0 END) as free_models,
  SUM(CASE WHEN models LIKE '%openrouter/%' AND models NOT LIKE '%:free%' THEN 1 ELSE 0 END) as paid_openrouter_models
FROM (
  SELECT name, json_each.value as models
  FROM combos, json_each(combos.models)
  WHERE name = 'channel-researcher'
)
GROUP BY name;
" 2>/dev/null
```

### Testing Actual Routing
```bash
# Get API key
KEY=$(grep "^OPENAI_API_KEY=" "$LOCALAPPDATA/hermes/.env" | cut -d= -f2)

# Test call to see which provider responds
curl -s http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "channel-researcher",
    "messages": [{"role": "user", "content": "What provider and model are you?"}],
    "max_tokens": 50
  }' | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Response from: {data.get('model', 'unknown')}\")
    print(f\"Provider indicator: {'gemini' in data.get('model','').lower() or 'openrouter' in data.get('model','').lower() or 'cloudflare' in data.get('model','').lower()}\")
    if 'usage' in data:
        print(f\"Cost: {data['usage'].get('cost', 0)}\")
except Exception as e:
    print(f\"Error: {e}\")
"
```

## Verification Checklist

### ✅ Discord Gateway Working
- [ ] Token exists in Local/.env
- [ ] Bot can fetch guild info via Discord API
- [ ] `hermes send --list discord` shows channels
- [ ] Test message delivers successfully

### ✅ 9Router Free Tier Active
- [ ] 9Router process running on port 20128
- [ ] `channel-researcher` combo contains >90% free models
- [ ] No `openrouter/` models without `:free` suffix
- [ ] Test call returns cost: 0
- [ ] Fallback routing works (multiple free providers)

### ✅ Cost Protection
- [ ] OpenRouter activity shows $0 spent
- [ ] No cloud API calls bypassing 9Router
- [ ] Sub-agents configured with `:free` explicit models
- [ ] Kiro credits usage: 0% (reserved for premium tasks only)

## Common Issues & Fixes

### Discord Token in Wrong Location
**Symptom**: Gateway runs but Discord disconnected
**Fix**: Copy token to correct .env file
```bash
# If token in Local but Hermes reads from Roaming
TOKEN=$(grep "^DISCORD_BOT_TOKEN=" "$LOCALAPPDATA/hermes/.env" | cut -d= -f2)
echo "DISCORD_BOT_TOKEN=$TOKEN" >> "$APPDATA/hermes/.env"
```

### 9Router Routing to Paid Models
**Symptom**: OpenRouter charges despite `:free` models
**Fix**: Clean combo to only free models
```python
# Python script to enforce free-only routing
import sqlite3, json, sys
db = r"C:\Users\arija\AppData\Roaming\9router\db\data.sqlite"
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute("SELECT id, models FROM combos WHERE name='channel-researcher'")
combo_id, models_json = cur.fetchone()
models = json.loads(models_json)

# Filter to only free providers
free_models = [
    m for m in models 
    if ':free' in m or 
       m.startswith(('kr/', 'kgw/', 'cf/', 'gc/', 'gemini/', 'groq/', 'kimi/', 'nvidia/', 'vx/'))
]

if len(free_models) < 5:
    free_models.extend([
        'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free',
        'openrouter/google/gemma-4-31b-it:free',
        'openrouter/groq/mixtral-8x7b-32768:free',
        'kgw/kwaipilot/kat-coder-pro-v2.5:free',
        'cf/@cf/meta/llama-3.3-70b-instruct-fp8-fast'
    ])

cur.execute("UPDATE combos SET models=? WHERE id=?", (json.dumps(free_models), combo_id))
conn.commit()
conn.close()
```