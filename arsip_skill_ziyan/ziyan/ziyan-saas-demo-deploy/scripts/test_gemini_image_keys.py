"""
Cek semua Gemini API key ke endpoint image generation.
Jalankan: python3 scripts/test_gemini_image_keys.py
Output: per-key status OK / HTTP 429 (quota) / 403 (invalid) / 404 (model).

P11 context: Gemini image free tier = hard account-level rate limit.
Semua key di akun sama akan 429. Tidak ada bypass via :predict atau 9Router.
"""
import json
import os
import urllib.request

# --- Ambil key dari env ---
KEYS = {}
for var in ("GEMINI_KEY", "GOOGLE_KEY", "GEMINI_KEYB2"):
    v = os.environ.get(var, "")
    if v:
        KEYS[var] = v

# --- Hardcode key Bos (dari AI Studio screenshot 2026-08-08) ---
HARD = {
    "keyb2_LFTg": "AQ.Ab8RN6LOi6WeRpHabsAvf6fORgBvb8nDsdWVuvzbqhHcp1LFTg",
    "gemini_cZrA": "AIzaSyBqrwpHaqKwiPbE34Qbp66EFClco1TcZrA",
}
KEYS.update(HARD)

URL = ("https://generativelanguage.googleapis.com/v1beta/models/"
       "gemini-2.5-flash-image:generateContent?key={key}")
BODY = json.dumps({
    "contents": [{"parts": [{"text": "a small red car"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}).encode()


def test(name, key):
    req = urllib.request.Request(URL.format(key=key), data=BODY,
                                 headers={"Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read().decode())
        parts = d.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        img = any(p.get("inlineData") for p in parts)
        return f"OK image={'YES' if img else 'NO(text only)'}"
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        code = e.code
        if code == 429:
            return "429 QUOTA (akun kena limit, cek setup billing / tunggu reset)"
        if code == 403:
            return "403 INVALID KEY"
        if code == 404:
            return "404 MODEL NOT FOUND (salah endpoint/model)"
        return f"HTTP {code}: {msg[:100]}"
    except Exception as e:
        return f"ERR {str(e)[:80]}"


if __name__ == "__main__":
    print("=== Gemini Image Key Check (P11) ===")
    if not KEYS:
        print("Tidak ada key ditemukan.")
    for n, k in KEYS.items():
        print(f"{n}: {test(n, k)}")
    print("\nCatatan: kalau semua 429 -> akun kena quota. Bypass = setup billing")
    print("di AI Studio, atau tunggu reset. JANGAN test :predict (404) / 9Router (no image model).")
