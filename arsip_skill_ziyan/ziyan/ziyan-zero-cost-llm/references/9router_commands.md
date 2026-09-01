# 9Router Quick Commands (ZIYAN $0)

## Start / Stop / Check
```bash
# Start (bash script, NOT node)
bash "C:/Users/arija/AppData/Roaming/npm/9router" --tray --no-browser

# Check alive (wait ~12s after start)
curl -s -m5 "http://127.0.0.1:20128/v1/models" \
  -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" > models.json

# Kill
PID=$(netstat -ano 2>/dev/null | grep ":20128" | head -1 | awk '{print $5}')
taskkill /F /PID $PID
```

## List free models
```bash
curl -s "http://127.0.0.1:20128/v1/models" -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" \
 | python3 -c "import sys,json; d=json.load(sys.stdin); [print(m['id']) for m in d['data'] if ':free' in m['id']]"
```

## Test $0 (must show "cost":0)
```bash
curl -s -m25 "http://127.0.0.1:20128/v1/chat/completions" \
  -H "Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openrouter/nvidia/nemotron-3-ultra-550b-a55b:free","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' \
 | python3 -c "import sys,json; d=json.load(sys.stdin); print('cost:', d['usage']['cost'])"
```

## DB combo cleanup (only :free)
```python
import sqlite3, json
db='C:/Users/arija/AppData/Roaming/9router/db/data.sqlite'
c=sqlite3.connect(db); cur=c.cursor()
cur.execute('SELECT id, models FROM combos')
for rid, m in cur.fetchall():
    ms=json.loads(m); free=[x for x in ms if ':free' in x]
    if not free: free=['openrouter/nvidia/nemotron-3-ultra-550b-a55b:free',
      'openrouter/google/gemma-4-31b-it:free','openrouter/groq/mixtral-8x7b-32768:free']
    cur.execute('UPDATE combos SET models=? WHERE id=?', (json.dumps(free), rid))
c.commit()
```
NOTE: edit SQLite DB, NOT the `9router-backup-*.json` snapshot in home dir.

## Fix sub-agent delegation (CLI only — config.yaml is protected)
```
hermes config set delegation.model "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"
hermes config set delegation.provider 9router
hermes config get delegation.model   # must return :free
```
PITFALL: `model: openrouter` (bare) → no route in 9Router → Hermes falls back to OpenRouter CLOUD (paid). Always use explicit `:free` model.
