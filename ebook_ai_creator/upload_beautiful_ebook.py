import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path("C:/Users/arija/ziyancorp/ebook_ai_creator")
output_html = ROOT / "Mesin_Pencetak_Uang_YouTube_Beautiful.html"
output_pdf = ROOT / "Mesin_Pencetak_Uang_YouTube_Beautiful.pdf"

if not output_html.exists():
    print(f"Error: {output_html} not found.")
    sys.exit(1)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print("[*] Printing HTML to PDF using Headless Chrome...")
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

# Upload to Google Drive
print("[*] Uploading to Google Drive...")
sys_path = Path('C:/Users/arija/ziyancorp/arsip_celine_aurel')
sys.path.append(str(sys_path))
from ziyan_bot.google_workspace import GoogleWorkspace
load_dotenv(sys_path / '.env')
gw = GoogleWorkspace(sys_path / 'credentials.json', sys_path / 'token.json', os.getenv('GOOGLE_ROOT_FOLDER_ID'), os.getenv('GOOGLE_SPREADSHEET_ID'))
res = gw.upload_file(output_pdf, os.getenv('GOOGLE_ROOT_FOLDER_ID'))
print('LINK: https://drive.google.com/file/d/' + res.get('id', '') + '/view')
