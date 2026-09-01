#!/usr/bin/env python3
"""Bulk image generator ZIYAN - gratis via 9router (ag/gemini-3.1-flash-image / Nano Banana 2).
Cara: python3 gen_img.py "prompt gambar" [nama_file_output]
Atau bulk: python3 gen_img.py --file prompts.txt  (1 prompt per baris)
"""
import sys, json, base64, os, requests, os as _os

URL = "http://127.0.0.1:20128/v1/images/generations"
MODEL = "ag/gemini-3.1-flash-image"
OUTDIR = "C:/Users/arija/ziyan_generated"
KEY = _os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")

os.makedirs(OUTDIR, exist_ok=True)

def gen(prompt, out_name=None):
    headers = {"Content-Type": "application/json"}
    if KEY:
        headers["Authorization"] = f"Bearer {KEY}"
    r = requests.post(URL, headers=headers, json={"model": MODEL, "prompt": prompt, "n": 1}, timeout=120)
    r.raise_for_status()
    data = r.json()
    img = None
    if "data" in data and data["data"]:
        item = data["data"][0]
        if "b64_json" in item:
            img = base64.b64decode(item["b64_json"])
        elif "url" in item:
            img = requests.get(item["url"]).content
    if not img:
        raise ValueError("Tidak ada field gambar di respons: " + str(data)[:200])
    fn = out_name or f"img_{abs(hash(prompt))%100000}.png"
    path = os.path.join(OUTDIR, fn)
    with open(path, "wb") as f:
        f.write(img)
    print(f"OK -> {path} ({len(img)} bytes)")

if __name__ == "__main__":
    if "--file" in sys.argv:
        fpath = sys.argv[sys.argv.index("--file")+1]
        with open(fpath, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        gen(line, f"img_{i:03d}.png")
                    except Exception as e:
                        print(f"FAIL baris {i}: {e}")
    elif len(sys.argv) > 1:
        gen(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print("Pakai: python3 gen_img.py \"prompt\" [nama.png]")
        print("Atau:  python3 gen_img.py --file prompts.txt")
