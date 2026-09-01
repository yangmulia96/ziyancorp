import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import requests
import subprocess
from pathlib import Path

ROOT = Path("C:/Users/arija/ziyancorp/ebook_ai_creator")
ROOT.mkdir(parents=True, exist_ok=True)

img_dir = ROOT / "sample_images"
img_dir.mkdir(exist_ok=True)

print("🎨 1. Mengunduh Ilustrasi 3D Premium...")

# Prompts for 3D Illustrations
images_to_fetch = [
    ("cover_3d.png", "https://image.pollinations.ai/prompt/3d%20cute%20boy%20character%20operating%20futuristic%20ai%20automation%20dashboard%20with%20golden%20coins%20and%20play%20buttons%20pop%20mart%20claymorphism%20pixar%20style%20vibrant%20octane%20render%208k?width=900&height=600&nologo=true&seed=42"),
    ("chapter1_3d.png", "https://image.pollinations.ai/prompt/3d%20isometric%20automated%20digital%20factory%20conveyor%20belt%20producing%20social%20media%20videos%20and%20floating%20glowing%20cards%20soft%20clay%20aesthetic%20pastel%20colors%20studio%20lighting?width=800&height=450&nologo=true&seed=108"),
    ("chapter2_3d.png", "https://image.pollinations.ai/prompt/3d%20chibi%20girl%20analyzing%20growth%20charts%20and%20view%20metrics%20on%20glowing%20glass%20screen%20pop%20mart%20cute%20aesthetic%20high%20quality%203d%20render?width=800&height=450&nologo=true&seed=225")
]

for fname, url in images_to_fetch:
    fpath = img_dir / fname
    if not fpath.exists() or fpath.stat().st_size < 5000:
        print(f" - Downloading {fname}...")
        try:
            r = requests.get(url, timeout=45)
            if r.status_code == 200:
                with open(fpath, "wb") as f:
                    f.write(r.content)
                print(f"   ✅ Saved {fname} ({len(r.content)/1024:.1f} KB)")
        except Exception as e:
            print(f"   ⚠️ Error fetching {fname}: {e}")

print("📄 2. Menyusun Template Majalah Editorial E-Book Bergambar...")

html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Pabrik Konten AI 24 Jam - Illustrated Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Cabinet+Grotesk:wght@800;900&display=swap');
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        .page {{
            width: 210mm;
            min-height: 297mm;
            padding: 20mm;
            margin: 0 auto 10mm auto;
            background: #ffffff;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            page-break-after: always;
            position: relative;
        }}
        
        /* COVER PAGE */
        .cover {{
            background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            padding: 25mm 20mm;
        }}
        
        .badge {{
            display: inline-block;
            padding: 8px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 30px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #38bdf8;
            backdrop-filter: blur(10px);
        }}
        
        .cover h1 {{
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 52px;
            font-weight: 900;
            line-height: 1.15;
            margin-top: 15px;
            margin-bottom: 10px;
            background: linear-gradient(to right, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }}
        
        .cover .subtitle {{
            font-size: 20px;
            color: #94a3b8;
            max-width: 600px;
            line-height: 1.5;
            font-weight: 500;
        }}
        
        .cover-img-box {{
            width: 100%;
            max-width: 520px;
            margin: 25px 0;
            border-radius: 24px;
            overflow: hidden;
            border: 3px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
        
        .cover-img-box img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .cover-footer {{
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            width: 100%;
            padding-top: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            color: #94a3b8;
        }}
        
        /* CONTENT PAGES */
        .header-tag {{
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #6366f1;
            margin-bottom: 6px;
        }}
        
        h2 {{
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 34px;
            font-weight: 900;
            color: #0f172a;
            line-height: 1.2;
            margin-bottom: 18px;
        }}
        
        .chapter-hero {{
            width: 100%;
            border-radius: 18px;
            overflow: hidden;
            margin: 15px 0 25px 0;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
        }}
        
        .chapter-hero img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        p {{
            font-size: 15.5px;
            line-height: 1.8;
            color: #334155;
            margin-bottom: 16px;
        }}
        
        /* 3D HIGHLIGHT CARD */
        .card-highlight {{
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border: 1px solid #bbf7d0;
            border-left: 5px solid #22c55e;
            border-radius: 14px;
            padding: 20px;
            margin: 22px 0;
        }}
        
        .card-highlight h4 {{
            color: #15803d;
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .card-highlight p {{
            margin-bottom: 0;
            color: #166534;
            font-size: 14.5px;
        }}
        
        .grid-2 {{
            display: flex;
            gap: 15px;
            margin: 20px 0;
        }}
        
        .grid-item {{
            flex: 1;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        
        .grid-item .num {{
            font-size: 24px;
            font-weight: 900;
            color: #6366f1;
            margin-bottom: 5px;
        }}
        
        .grid-item h5 {{
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 6px;
        }}
        
        .grid-item p {{
            font-size: 13px;
            line-height: 1.6;
            color: #64748b;
            margin-bottom: 0;
        }}
        
        .page-num {{
            position: absolute;
            bottom: 12mm;
            right: 20mm;
            font-size: 12px;
            font-weight: 700;
            color: #94a3b8;
        }}
    </style>
</head>
<body>

    <!-- HALAMAN 1: COVER DENGAN ILUSTRASI 3D -->
    <div class="page cover">
        <div>
            <span class="badge">Edisi Eksklusif ZiyanCorp</span>
            <h1>Pabrik Konten AI<br>Otomatis 24 Jam</h1>
            <p class="subtitle">Panduan Praktis Membangun Kerajaan Konten YouTube & Medsos Tanpa Perlu Menampakkan Wajah</p>
        </div>
        
        <div class="cover-img-box">
            <img src="{str(img_dir / 'cover_3d.png').replace(os.sep, '/')}" alt="3D Cover">
        </div>
        
        <div class="cover-footer">
            <span>Penulis: <b>ZiyanCorp Publishing</b></span>
            <span>Standard Blueprint 2026</span>
        </div>
    </div>

    <!-- HALAMAN 2: BAB 1 DENGAN ILUSTRASI 3D ISOMETRIC -->
    <div class="page">
        <div class="header-tag">BAB 01 — REVOLUSI AUTOMATION</div>
        <h2>Mindset Sutradara: Bekerja Cerdas dengan Armada AI</h2>
        
        <div class="chapter-hero">
            <img src="{str(img_dir / 'chapter1_3d.png').replace(os.sep, '/')}" alt="3D Chapter 1">
        </div>
        
        <p>Banyak kreator pemula terjebak dalam lingkaran setan kelelahan (*burnout*). Mereka menghabiskan 6 jam hanya untuk mengedit 1 video, mencari footage, merekam suara, hingga akhirnya menyerah sebelum melihat hasilnya.</p>
        
        <div class="card-highlight">
            <h4>💡 Aturan Emas ZiyanCorp:</h4>
            <p>Kita tidak bekerja sebagai buruh editor. Kita adalah <b>Sutradara & Arsitek Sistem</b>. Seluruh pekerjaan teknis (riset naskah, pencarian video 4K, dubbing suara, hingga penataan subtitle) diserahkan 100% kepada armada AI dan script otomatis.</p>
        </div>
        
        <div class="grid-2">
            <div class="grid-item">
                <div class="num">01</div>
                <h5>Riset Topik Otomatis</h5>
                <p>Gemini AI membedah tren algoritma global dan meracik hook 3 detik dengan retensi penonton di atas 85%.</p>
            </div>
            <div class="grid-item">
                <div class="num">02</div>
                <h5>Render di Cloud GPU</h5>
                <p>Google Colab memproses video 4K, efek audio ducking, dan transisi tanpa membebani prosesor laptop.</p>
            </div>
        </div>
        
        <p>Dengan sistem ini, membuat 3–5 video berkualitas tinggi per hari bukan lagi hal yang melelahkan, melainkan proses yang berjalan secara instan di latar belakang.</p>
        
        <div class="page-num">01</div>
    </div>

    <!-- HALAMAN 3: BAB 2 DENGAN ILUSTRASI 3D ANALYTICS -->
    <div class="page">
        <div class="header-tag">BAB 02 — MONETISASI & ANALITIK</div>
        <h2>Menembus Algoritma Global: Dari 0 ke 100M Views</h2>
        
        <div class="chapter-hero">
            <img src="{str(img_dir / 'chapter2_3d.png').replace(os.sep, '/')}" alt="3D Chapter 2">
        </div>
        
        <p>Algoritma YouTube Shorts tidak memilih video berdasarkan keberuntungan. Semuanya adalah kalkulasi matematika dari dua metrik utama: <b>Viewed vs Swiped Away (VVSA)</b> dan <b>Average Percentage Viewed (APV)</b>.</p>
        
        <p>Ketika video Anda memiliki subtitle kotak kuning dengan kontras tinggi dan alur cerita <i>seamless loop</i>, penonton secara psikologis akan menonton hingga selesai bahkan mengulanginya tanpa sadar.</p>
        
        <div class="card-highlight" style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-color: #bfdbfe; border-left-color: #3b82f6;">
            <h4 style="color: #1d4ed8;">📈 Kunci Dominasi Pasar Luar Negeri (US & Global):</h4>
            <p style="color: #1e40af;">Gunakan narasi bahasa Inggris berkualitas studio (seperti Christopher Neural) dan targetkan jam tayang saat warga Amerika sedang aktif di jam istirahat dan pulang kerja untuk meraup nilai RPM/AdSense tertinggi.</p>
        </div>
        
        <div class="page-num">02</div>
    </div>

</body>
</html>
"""

out_html = ROOT / "Sample_Illustrated_Ebook.html"
out_html.write_text(html_content, encoding="utf-8")
print(f"✅ HTML E-Book Bergambar Siap: {out_html}")

# Print to PDF via Headless Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

out_pdf = ROOT / "Sample_Illustrated_Ebook.pdf"
if os.path.exists(chrome_path):
    print("🖨️ 3. Mencetak ke PDF Kualitas Vektor...")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={out_pdf}",
        str(out_html)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🎉 SUKSES! PDF E-Book Bergambar 3D Tercipta: {out_pdf} ({out_pdf.stat().st_size / (1024*1024):.2f} MB)")
