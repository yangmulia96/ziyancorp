# Multi-Platform Posting Fix (2026-08-10)

## Issue: Instagram Detection Failed, Agent Running FB + YouTube Only

### Root Cause
- `instagram.ig_user_id` in `config.yaml` was empty `""`
- `get_ig_user_id()` in `ig_upload.py` relied on auto-discovery via `GET /me?fields=instagram_business_account`
- Primary FB Page token (ke-1) returned 400 Bad Request
- Token ke-2 works but agent doesn't use it for auto-discovery

### Fix Applied
Set `ig_user_id` directly in `config.yaml`:

```yaml
instagram:
  access_token: ""
  ig_user_id: "17841479944713462"   # SET LANGSUNG
  token_file_path: "C:/Users/arija/OneDrive/ziyan_pending/fb_page_token.txt"

runtime:
  fb_page_id: ""
  ig_user_id: "17841479944713462"   # SET LANGSUNG
```

### Verification
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

### Result
Agent log now shows: `INFO - Instagram Business Account connected` instead of `ERROR - No Instagram Business Account linked to this FB Page`

### Key Learning
After Meta Business Suite approval, **always set `ig_user_id` directly in config.yaml** — don't rely on auto-discovery which can fail due to token permission differences.