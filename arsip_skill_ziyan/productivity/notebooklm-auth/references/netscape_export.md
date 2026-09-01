# NotebookLM Netscape Cookie Export — Working Path (Windows 10)

The ONLY reliable auth path on this host. DPAPI (`--browser-cookies`) and
`login --fresh` both FAIL (see SKILL.md). Use browser Netscape export instead.

## Step 1: User exports cookies
1. Open `notebooklm.google.com` in Brave/Chrome already logged in as `mziyan266@gmail.com`.
2. Confirm the dashboard loads (session is warm).
3. Use extension "Get cookies.txt LOCALLY" → export **Netscape format**.
4. Save as `C:\Users\arija\Downloads\cookies.txt`.
   - Export FROM the notebooklm.google.com tab so `__Secure-1PSIDTS` is captured.

## Step 2: convert_netscape_cookies.py (save to C:\Users\arija)
```python
import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_netscape_cookies.py <cookies.txt> [output.json]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "storage_state.json"
    cookies = []
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain_field, include_sub, path, secure, expiry, name, value = parts[:7]
            http_only = domain_field.startswith("#HttpOnly_")
            domain = domain_field.replace("#HttpOnly_", "")
            is_secure = secure.lower() == "true"
            cookies.append({
                "name": name,
                "value": value,
                "domain": domain,
                "path": path,
                "expires": int(expiry) if (expiry.isdigit() and int(expiry) > 0) else -1,
                "httpOnly": http_only,
                "secure": is_secure,
                "sameSite": "Lax",
            })
    storage = {"cookies": cookies, "origins": []}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=2)
    print(f"Converted {len(cookies)} cookies -> {output_path}")

if __name__ == "__main__":
    main()
```

## Step 3: sync_notebooklm_auth.bat (double-click after re-export)
```bat
@echo off
cd /d C:\Users\arija
set VENV=C:\Users\arija\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
findstr /i "google.com google.co.id notebook.google youtube.com accounts.google blogger.com" "Downloads\cookies.txt" > "Downloads\cookies_google.txt"
"%VENV%" convert_netscape_cookies.py "Downloads\cookies_google.txt" ".notebooklm\profiles\default\storage_state.json"
"%VENV%" -m notebooklm auth check --test
pause
```

## Step 4: verify with LIVE call (auth check alone is a false positive)
```
notebooklm list   # must return notebooks, not "Authentication expired"
```

## Re-auth cadence
Cookie goes stale when Google rotates it. When `notebooklm list` / `add-research`
fails with "Authentication expired", repeat Steps 1-3.
