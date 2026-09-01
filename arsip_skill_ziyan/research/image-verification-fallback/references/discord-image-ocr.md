# Discord / Messaging-Gateway Image Recovery (tested on this host)

## When this applies
User sends an image via Discord / Telegram / WhatsApp gateway and you must read its content.
`vision_analyze` returns 404 on this host because the active model (`tencent/hy3:free`) has **no native vision** and the aux vision model is down.

## HARD RULE
- **DO NOT suggest `computer_use`** to read gateway images. `computer_use` drives the LOCAL Windows desktop and cannot see attachments the user sent through the chat gateway. Suggesting it repeatedly is a repeated mistake — stop.
- **Load this skill (`image-verification-fallback`) and go straight to OCR.**

## Environment facts (verified this session)
- Tesseract is ALREADY installed at `C:\Program Files\Tesseract-OCR\tesseract.exe` — skip `winget install`.
- Hermes agent venv (`AppData\Local\hermes\hermes-agent\venv`) has a **broken PIL** (`cannot import name '_imaging'`). Do NOT use it for OCR.
- 9router proxy (71 models in `models9r.json`, channels gemini/groq/kimi/kr/openrouter/root) has **NO vision models** — `gemini/` channel is also dead (400 invalid key). Do NOT route screenshots through 9router for reading.
- PDFs: `pdftotext` (mingw64) works directly: `pdftotext file.pdf -`. PyPDF2/pypdf are NOT installed in base venv.

## Tested OCR recipe (recovered a GCP "You need additional access" error screenshot)
```bash
cd /c/Users/arija
uv venv ocr_env
uv pip install --python ocr_env pytesseract pillow
cat > ocr_script.py <<'PY'
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
img = Image.open(r"<path>").resize((img.width*2, img.height*2))
print(pytesseract.image_to_string(img).strip())
PY
uv run --python ocr_env python ocr_script.py
```
Upscaling 2x before OCR improves accuracy on UI screenshots.

## PDFs from gateway
`pdftotext file.pdf -` → parse text. A React/JSX PDF this session yielded clean code after:
1. re-decode latin-1→utf-8 (pdftotext emitted a `0xb7` byte),
2. strip `\f` page-break artifacts,
3. strip leading ```react / trailing ``` fence markers.

## Decision after OCR
- If the image is a settings/error page (e.g. GCP "additional access" dialog), act on the recovered text.
- Never `rm` the source image before confirming the recovered text with the user.
