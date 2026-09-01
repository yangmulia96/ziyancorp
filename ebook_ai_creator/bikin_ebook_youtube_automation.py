import os
import sys
import markdown
import subprocess
from pathlib import Path
from google import genai
from dotenv import load_dotenv

ROOT = Path("C:/Users/arija/ziyancorp/ebook_ai_creator")
load_dotenv(ROOT.parent / "arsip_celine_aurel" / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY tidak ditemukan")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

title = "Mesin Pencetak Uang YouTube"
author = "ZiyanCorp Publishing"

prompt_extra = """
Buatkan isi E-Book tutorial lengkap untuk pemula tentang cara membangun pabrik video YouTube otomatis (hourly) menggunakan n8n (no code).
Pembahasan harus mencakup:
1. Mindset Automation (Kita sebagai sutradara, AI sebagai pekerja).
2. Persiapan: n8n, Google Sheets, openAI API (ChatGPT).
3. Cara kerja: Ide di Google Sheets -> n8n membaca data -> ChatGPT menulis script -> AI Video/Audio Generator (Suno/JSONToVideo) -> Auto Upload YouTube.
4. Langkah-langkah praktis dan mudah dipahami oleh orang awam (tanpa coding).

Buat dalam bahasa Indonesia yang gaul, asik, tapi sangat daging dan profesional. 
Gunakan format Markdown (Heading 2, 3, bullet points). JANGAN gunakan tag ```markdown di awal/akhir teks. Isi harus panjang.
"""

def generate_content():
    print("[*] Executing Gemini Pro for content...")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt_extra,
    )
    return response.text.replace("```markdown", "").replace("```", "")

def generate_description():
    print("[+] Executing Gemini Flash for description...")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Buat 1 halaman kata pengantar (sekitar 3-4 paragraf) yang menggugah untuk E-book berjudul '{title}' tentang cara bikin pabrik video AI otomatis pakai n8n. Tutup dengan kalimat selamat membaca dari '{author}'. JANGAN gunakan tag markdown block.",
    )
    return response.text.replace("```markdown", "").replace("```", "").strip()

output_pdf = ROOT / "Mesin_Pencetak_Uang_YouTube.pdf"
output_html = ROOT / "Mesin_Pencetak_Uang_YouTube.html"

desc = generate_description()
desc_html = markdown.markdown(desc)
md_content = generate_content()
html_content = markdown.markdown(md_content)

html_template = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap');
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            margin: 0;
            padding: 0;
            color: #1f2937;
            background-color: #fff;
        }
        .cover {
            height: 297mm;
            width: 210mm;
            background: linear-gradient(135deg, #1e3a8a 0%, #e11d48 100%);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            page-break-after: always;
            padding: 40px;
            box-sizing: border-box;
        }
        .cover h1 {
            font-size: 64px;
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.2;
            text-transform: uppercase;
        }
        .cover .author {
            font-size: 24px;
            font-weight: 400;
            opacity: 0.9;
            margin-top: 50px;
            padding: 15px 40px;
            border-top: 2px solid rgba(255,255,255,0.3);
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        .page {
            padding: 20mm;
            page-break-after: always;
        }
        .intro {
            background-color: #f3f4f6;
            padding: 30px;
            border-radius: 15px;
            font-size: 18px;
            line-height: 1.8;
            margin-bottom: 40px;
            border-left: 5px solid #e11d48;
        }
        h2 { color: #e11d48; font-size: 32px; margin-top: 40px; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; page-break-before: always; }
        h2:first-of-type { page-break-before: auto; }
        h3 { color: #374151; font-size: 24px; margin-top: 25px; }
        p, li { font-size: 18px; line-height: 1.8; margin-bottom: 15px; color: #4b5563; }
    </style>
</head>
<body>
    <div class="cover">
        <h1>__TITLE__</h1>
        <div class="author">__AUTHOR__</div>
    </div>
    <div class="page">
        <div class="intro">
            <h2 style="margin-top:0; border:none; color:#1e3a8a;">Kata Pengantar</h2>
            __DESC__
        </div>
    </div>
    <div class="page">
        __CONTENT__
    </div>
</body>
</html>
"""

html_template = html_template.replace("__TITLE__", title)
html_template = html_template.replace("__AUTHOR__", author)
html_template = html_template.replace("__DESC__", desc_html)
html_template = html_template.replace("__CONTENT__", html_content)

output_html.write_text(html_template, encoding="utf-8")
print(f"[*] HTML Created: {output_html.name}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

if os.path.exists(chrome_path):
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={output_pdf}",
        str(output_html)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SUCCESS] PDF Created: {output_pdf.name}")


