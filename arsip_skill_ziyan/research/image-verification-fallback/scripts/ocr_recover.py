#!/usr/bin/env python3
"""Deterministic OCR recovery for images the user sends via Discord/Discord gateway.

Why: active Hermes model (tencent/hy3:free) has NO native vision, and the aux
vision model 404s in this environment. OCR via tesseract is the reliable path.
Tesseract is ALREADY installed at C:\Program Files\Tesseract-OCR\tesseract.exe.
Hermes venv PIL is broken (_imaging import error) -> use uv venv.

Usage (from C:\Users\arija):
  uv venv ocr_env
  uv pip install --python ocr_env pytesseract pillow
  uv run --python ocr_env python ocr_recover.py <image_path>

Prints extracted text. Never invents content it did not read.
"""
import sys, subprocess, os

IMG = sys.argv[1] if len(sys.argv) > 1 else None
if not IMG or not os.path.exists(IMG):
    print("ERROR: berikan path gambar sebagai argumen")
    sys.exit(2)

# ensure venv + deps
subprocess.run("uv venv ocr_env", shell=True, check=False)
subprocess.run("uv pip install --python ocr_env pytesseract pillow", shell=True, check=False)

script = f'''
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
from PIL import Image
img = Image.open(r"{IMG}").convert("RGB")
img = img.resize((img.width*2, img.height*2))
print(pytesseract.image_to_string(img).strip())
'''
out = subprocess.run(f'uv run --python ocr_env python -c "{script}"',
                     shell=True, capture_output=True, text=True)
print(out.stdout.strip() or out.stderr.strip())
