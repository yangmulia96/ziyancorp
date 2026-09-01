# 9Router via requests (Python) — Bearer + SSE

## Endpoint
POST http://127.0.0.1:20128/v1/chat/completions

## Auth
Header wajib: `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`
(Tanpa header → `{"error":"Missing API key"}`. Key ada di env `HERMES_CUSTOM_9ROUTER_API_KEY`, len ~35.)

## SSE gotcha
9Router mengembalikan **SSE** (`data: {json}\n\n` per chunk) meski `stream: False` dikirim.
`r.json()` GAGAL (bukan JSON utuh). Parse manual:

```python
import os, requests, json
key = os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
r = requests.post("http://127.0.0.1:20128/v1/chat/completions", headers=headers,
                  json={"model":"kr/claude-sonnet-4.5","messages":[{"role":"user","content":prompt}],
                        "max_tokens":300,"temperature":0.8,"stream":False}, timeout=40)
text = r.text
if text.strip().startswith("data:"):
    content = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("data:") and "[DONE]" not in line:
            try:
                obj = json.loads(line[5:].strip())
                content += obj["choices"][0]["delta"].get("content","")
            except: pass
    caption = content.strip()
else:
    caption = r.json()["choices"][0]["message"]["content"].strip()
```

## Verify model live
`curl -s -m5 http://127.0.0.1:20128/health` → kosong = 9Router mati.
Caption natural (bukan robotik) untuk produk: prompt gaya "tulis kayak orang beneran rekomendasiin ke temen, santai, 1 emoji max, sertakan link". Untuk AI-influencer (Celine Aurel): format [link] → [deskripsi 1-2 kalimat sebut ukuran/situasi] → [link lain] → [5 hashtag], JANGAN sebut harga.
