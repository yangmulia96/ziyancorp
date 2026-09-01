# 9Router Diagnostic & Combo Repair — Verified 2026-08-10

## DB Location
`C:\Users\arija\AppData\Roaming\9router\db\data.sqlite`

Tables:
- `combos` — kolom `models` = JSON array of model IDs (this is what `channel-researcher` resolves to)
- `providerConnections` — kolom `provider, name, testStatus, errorCode, backoffLevel, lastError, isActive`

## Diagnosis commands
```bash
DB="$APPDATA/9router/db/data.sqlite"
sqlite3 "$DB" "SELECT provider, testStatus, errorCode, backoffLevel, substr(lastError,1,90) FROM providerConnections;"
sqlite3 "$DB" "SELECT models FROM combos WHERE name='channel-researcher';"
```

## Provider status 2026-08-10
| Provider | Status | Error | Action |
|----------|--------|-------|--------|
| kgw / kilo-gateway | OK | nemotron-3-ultra-550b:free jalan | keep |
| openrouter | OK (sebagian) | deepseek-r1:free jadi PAID (404) | filter paid |
| groq | BROKEN | Invalid API Key (key rusak di .env) | refresh key |
| cloudflare-ai | BROKEN | Authentication error (key expired) | refresh key |
| gemini | 429 | quota exceeded | disable |
| antigravity | 429 | Individual quota reached | disable |
| kimi | 402 | membership unverified | disable |
| vertex | 401 | API key not supported | disable |
| nvidia (via OR) | 429/502 | 32/32 worker limit | fallback only |

## Fix procedure
1. Backup DB: `cp "$DB" "$DB.bak_diag_$(date +%Y%m%d_%H%M%S)"`
2. Disable dead providers: `UPDATE providerConnections SET isActive=0 WHERE provider IN ('antigravity','gemini','kimi','nvidia','vertex');`
3. Reorder combo to only-live free models (KGW priority 1):
```sql
UPDATE combos SET models='["kgw/nvidia/nemotron-3-ultra-550b-a55b:free","kgw/kilo-auto/free","kilo-gateway/kilo-auto/free","openrouter/nvidia/nemotron-3-ultra-550b-a55b:free","kr/claude-sonnet-4.5","kr/claude-opus-4.7","kr/deepseek-3.2"]', updatedAt='<now>' WHERE name='channel-researcher';
```
4. No restart needed for SQLite writes (9Router reads DB per request), but if combo still stale: restart 9router (`taskkill /F /IM 9router.exe` then `bash 9router --tray --no-browser`).

## Verified-live free models (priority order)
1. `kgw/nvidia/nemotron-3-ultra-550b-a55b:free`
2. `kgw/kilo-auto/free`
3. `kilo-gateway/kilo-auto/free`
4. `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`
5. `kr/claude-sonnet-4.5` (Kilo, not cloud)
6. `kr/claude-opus-4.7`

## JSON parse quirk (9Router local)
Response has leading whitespace + trailing `data: [DONE]`. Never `json.load()` raw.
```python
raw = curl_output
s = raw.find("{")
e = raw.rfind("}")
d = json.loads(raw[s:e+1])
```
Or shell: `| tr '\r' '\n' | grep '^{' | tail -1 | python3 -c "..."`
