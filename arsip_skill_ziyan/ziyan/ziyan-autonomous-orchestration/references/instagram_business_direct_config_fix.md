# Instagram Business Account Direct Config Fix (2026-08-10)

## Masalah
Agent Python `ziyan_affiliate_agent` gagal detek Instagram Business Account via auto-discovery:
- Graph API `GET /me?fields=instagram_business_account` dengan **token utama (ke-1)** return **400 Bad Request**
- Token ke-2 jalan (200 OK) tapi agent hanya pakai token ke-1 untuk auto-discovery
- Log: `ERROR - No Instagram Business Account linked to this FB Page` → agent jalan FB only

## Root Cause
- FB Page "Celine Aurel" punya 2+ Page Access Token
- Token ke-1 (yang di config.yaml `page_access_token`) tidak punya permission `instagram_business_account` → 400
- Token ke-2 (di `ziyan_fb_credentials.env` di Hermes config dir) punya permission → 200 OK return IG ID
- Agent config hanya set 1 token → auto-discovery gagal

## Fix: Set IG Business Account ID Langsung di config.yaml
```yaml
instagram:
  access_token: ""
  ig_user_id: "17841479944713462"   # SET LANGSUNG
  token_file_path: "C:/Users/arija/OneDrive/ziyan_pending/fb_page_token.txt"

runtime:
  fb_page_id: ""
  ig_user_id: "17841479944713462"   # SET LANGSUNG
```

## Verifikasi Cepat (Ad-hoc)
```bash
cd /c/Users/arija/ziyan_agent && .venv/Scripts/python.exe -c "
import sys, asyncio, yaml
sys.path.insert(0, r'C:\\Users\\arija\\ziyan_agent')
from modules.ig_upload import InstagramUploader

async def verify_ig():
    with open(r'C:\\Users\\arija\\ziyan_agent\\config.yaml') as f:
        config = yaml.safe_load(f)
    uploader = InstagramUploader(config)
    ig_id = await uploader.get_ig_user_id()
    await uploader.close()
    print(f'IG User ID: {ig_id}')
    print(f'Match: {ig_id == \"17841479944713462\"}')

asyncio.run(verify_ig())
"
# Output: IG User ID: 17841479944713462 | Match: True
```

## Catatan Penting
- Token FB yang sama (Page token) dipakai untuk upload IG via FB Graph API
- IG Business Account share token dengan FB Page yang linked
- Setelah approve di Meta Business Suite, **langsung set `ig_user_id` di config.yaml** — jangan andalkan auto-discovery
- File `ziyan_fb_credentials.env` di `C:\Users\arija\AppData\Local\hermes\` berisi token ke-2 + IG_ACCOUNT_ID untuk referensi manual