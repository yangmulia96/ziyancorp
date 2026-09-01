import os
import sys
from pathlib import Path
from google import genai
from dotenv import load_dotenv

ROOT = Path("C:/Users/arija/ziyancorp/ebook_ai_creator")
load_dotenv(ROOT.parent / "arsip_celine_aurel" / ".env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

template_path = Path("C:/Users/arija/.gemini/antigravity/brain/8edc1fac-574f-4d68-96a7-ededc6405215/ebook_ai_creator.html")
if not template_path.exists():
    print(f"Error: {template_path} not found.")
    sys.exit(1)

html_template = template_path.read_text(encoding="utf-8")

prompt = f"""
You are an expert E-Book writer and HTML designer.
I have an HTML file that contains a beautifully designed E-Book template (with a sidebar, hero section, module sections, step grids, and prompt containers).

Your task:
Write a BRAND NEW E-Book titled "Mesin Pencetak Uang YouTube: Cara Membangun Pabrik Video AI Otomatis Tanpa Coding".
The book is about building a fully automated YouTube faceless channel using n8n, Google Sheets, ChatGPT, and Suno/Video generators.

Instructions:
1. Rewrite the ENTIRE HTML file provided below.
2. Change the Title, Subtitle, Sidebar navigation links, and all the Module sections to match the new topic.
3. Keep ALL the CSS (`<style>`) and JavaScript (`<script>`) exactly as they are.
4. Keep the HTML structure (`<div class="card">`, `<div class="step-grid">`, `<div class="prompt-container">`, etc.) but fill them with the new content.
5. The new content should have at least 5-6 modules (e.g., Mindset, Persiapan n8n, Cara Kerja Google Sheets, AI Video Generation, Monetisasi).
6. Provide the complete HTML output starting with `<!DOCTYPE html>`. Do NOT wrap it in ```html markdown blocks.

Here is the original HTML template to base your structure on:

{html_template}
"""

print("[*] Generating new HTML E-book using gemini-3.6-flash...")
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
)

result_html = response.text.replace("```html", "").replace("```", "").strip()

output_html = ROOT / "Mesin_Pencetak_Uang_YouTube_Beautiful.html"
output_html.write_text(result_html, encoding="utf-8")
print(f"[SUCCESS] HTML Created: {output_html}")
