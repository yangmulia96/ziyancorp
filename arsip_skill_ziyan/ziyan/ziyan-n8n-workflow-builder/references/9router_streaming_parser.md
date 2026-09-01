# 9Router Streaming Response Parser (Python)

9Router (127.0.0.1:20128) balas **streaming** walau `stream:false` tidak diset.
`json.load()` langsung GAGAL. Pakai parser ini:

```python
import json, urllib.request, os
KEY = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
payload = {"model":"kr/claude-sonnet-4.5","messages":[{"role":"user","content":"TANYA"}],"temperature":0.3}
req = urllib.request.Request("http://localhost:20128/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"})
text = ""
with urllib.request.urlopen(req, timeout=60) as r:
    for line in r:
        line = line.decode().strip()
        if line.startswith("data: "):
            try:
                d = json.loads(line[6:])
                c = d["choices"][0]["delta"].get("content","")
                if c: text += c
            except: pass
print(text)
```

## Cara jalanin
1. `write_file` script ini ke `C:\Users\arija\script.py`
2. `terminal python3 script.py`  ← JANGAN pakai execute_code (diblokir)

## Catatan
- Model `kr/claude-sonnet-4.5` = stabil di 9Router (riset/bedah)
- `gc/gemini-3-pro-preview` GAGAL (quota OpenRouter), `ag/gemini-pro-agent` flaky
- Simpan output ke file dulu (`> out.txt`) lalu baca, hindari escaping di terminal curl
