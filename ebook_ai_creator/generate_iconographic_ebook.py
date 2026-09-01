import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path("C:/Users/arija/ziyancorp/ebook_ai_creator")
ROOT.mkdir(parents=True, exist_ok=True)

print("📝 1. Menyusun E-Book dengan Ilustrasi Icon Vektor & Diagram Modern...")

# Inlined clean SVG icons
ICON_MICROSCOPE = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 22h18"/><path d="m14 22 1-4H9l1 4"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="m12 6 3-3 3 3-3 3Z"/></svg>"""

ICON_CPU = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>"""

ICON_CLOUD = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>"""

ICON_ROCKET = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>"""

ICON_SHIELD = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>"""

ICON_TARGET = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>"""

ICON_LIGHTBULB = """<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>"""

ICON_ARROW_RIGHT = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>"""

html_doc = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Pabrik Konten AI - Edition with Tech Icon Illustrations</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            color: #0f172a;
            background-color: #f1f5f9;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        .page {{
            width: 210mm;
            min-height: 297mm;
            padding: 22mm 20mm;
            margin: 0 auto 10mm auto;
            background: #ffffff;
            page-break-after: always;
            position: relative;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}
        
        /* COVER PAGE */
        .cover {{
            background: radial-gradient(circle at top right, #1e3a8a 0%, #0f172a 60%, #020617 100%);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: flex-start;
            padding: 25mm 22mm;
        }}
        
        .brand-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            background: rgba(37, 99, 235, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.4);
            border-radius: 30px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: #60a5fa;
            text-transform: uppercase;
        }}
        
        .cover h1 {{
            font-size: 48px;
            font-weight: 900;
            line-height: 1.15;
            margin: 25px 0 15px 0;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: -0.5px;
        }}
        
        .cover h1 span {{
            color: #38bdf8;
        }}
        
        .cover-subtitle {{
            font-size: 18px;
            color: #94a3b8;
            line-height: 1.6;
            max-width: 580px;
            margin-bottom: 30px;
        }}
        
        /* COVER DIAGRAM HERO */
        .cover-diagram {{
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 24px;
            backdrop-filter: blur(12px);
            margin: 20px 0;
        }}
        
        .diagram-title {{
            font-size: 13px;
            font-weight: 800;
            color: #94a3b8;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 18px;
            text-align: center;
        }}
        
        .cover-flow {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }}
        
        .flow-node {{
            flex: 1;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 14px;
            padding: 16px 12px;
            text-align: center;
        }}
        
        .flow-icon-circle {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563eb, #0284c7);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px auto;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }}
        
        .flow-node h5 {{
            font-size: 13px;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 3px;
        }}
        
        .flow-node p {{
            font-size: 11px;
            color: #94a3b8;
        }}
        
        .flow-arrow {{
            color: #38bdf8;
            font-size: 20px;
            font-weight: 900;
        }}
        
        .cover-footer {{
            width: 100%;
            border-top: 1px solid rgba(255, 255, 255, 0.12);
            padding-top: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: #94a3b8;
        }}
        
        /* CONTENT PAGES */
        .chapter-tag {{
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #2563eb;
            margin-bottom: 8px;
        }}
        
        h2 {{
            font-size: 30px;
            font-weight: 900;
            color: #0f172a;
            line-height: 1.25;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
        }}
        
        p {{
            font-size: 15px;
            line-height: 1.75;
            color: #475569;
            margin-bottom: 18px;
        }}
        
        /* FEATURE CARDS WITH CIRCULAR ICON BADGES */
        .feature-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 24px 0;
        }}
        
        .feature-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 20px;
            display: flex;
            align-items: flex-start;
            gap: 16px;
            transition: all 0.2s;
        }}
        
        .icon-badge-blue {{
            flex-shrink: 0;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
        }}
        
        .icon-badge-sky {{
            flex-shrink: 0;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
        }}
        
        .icon-badge-indigo {{
            flex-shrink: 0;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
        }}
        
        .icon-badge-teal {{
            flex-shrink: 0;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            box-shadow: 0 4px 10px rgba(13, 148, 136, 0.25);
        }}
        
        .feature-card-content h4 {{
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 5px;
        }}
        
        .feature-card-content p {{
            font-size: 13.5px;
            line-height: 1.55;
            color: #64748b;
            margin-bottom: 0;
        }}
        
        /* HORIZONTAL WORKFLOW STEP DIAGRAM */
        .workflow-box {{
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 18px;
            padding: 22px 20px;
            margin: 26px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }}
        
        .workflow-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .workflow-header h5 {{
            font-size: 14px;
            font-weight: 800;
            color: #1e293b;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .pill-badge {{
            background: #dbeafe;
            color: #1d4ed8;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
        }}
        
        .workflow-steps {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}
        
        .step-item {{
            flex: 1;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 10px;
            text-align: center;
        }}
        
        .step-icon-sm {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: #eff6ff;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 8px auto;
        }}
        
        .step-item h6 {{
            font-size: 12px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 2px;
        }}
        
        .step-item span {{
            font-size: 10.5px;
            color: #64748b;
        }}
        
        .step-arrow {{
            color: #94a3b8;
            display: flex;
            align-items: center;
        }}
        
        /* CALLOUT BOX WITH ICON */
        .callout-box {{
            background: #eff6ff;
            border-left: 5px solid #2563eb;
            border-radius: 12px;
            padding: 18px 20px;
            margin: 22px 0;
            display: flex;
            align-items: flex-start;
            gap: 16px;
        }}
        
        .callout-icon {{
            color: #2563eb;
            flex-shrink: 0;
            margin-top: 2px;
        }}
        
        .callout-box h5 {{
            font-size: 15px;
            font-weight: 800;
            color: #1e40af;
            margin-bottom: 4px;
        }}
        
        .callout-box p {{
            font-size: 13.5px;
            line-height: 1.6;
            color: #1e3a8a;
            margin-bottom: 0;
        }}
        
        /* KPI METRIC CARDS */
        .kpi-row {{
            display: flex;
            gap: 14px;
            margin: 22px 0;
        }}
        
        .kpi-card {{
            flex: 1;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px;
            text-align: center;
        }}
        
        .kpi-number {{
            font-size: 28px;
            font-weight: 900;
            color: #2563eb;
            line-height: 1.1;
            margin-bottom: 4px;
        }}
        
        .kpi-label {{
            font-size: 12px;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .page-footer {{
            position: absolute;
            bottom: 12mm;
            left: 20mm;
            right: 20mm;
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            font-weight: 700;
            color: #94a3b8;
            border-top: 1px solid #f1f5f9;
            padding-top: 10px;
        }}
    </style>
</head>
<body>

    <!-- HALAMAN 1: COVER TECH MINIMALIS DENGAN DIAGRAM ALUR VESTOR -->
    <div class="page cover">
        <div>
            <div class="brand-badge">
                {ICON_CPU} ZiyanCorp Automation Blueprint 2026
            </div>
            <h1>PABRIK KONTEN <span>AI 24 JAM</span></h1>
            <p class="cover-subtitle">Arsitektur Otomatisasi Video YouTube Shorts, Optimasi Algoritma Retensi, dan Monetisasi Skala Global.</p>
        </div>
        
        <!-- DIAGRAM ARSITEKTUR DI COVER -->
        <div class="cover-diagram">
            <div class="diagram-title">PIPELINE OTOMATISASI PRODUKSI CLOUD</div>
            <div class="cover-flow">
                <div class="flow-node">
                    <div class="flow-icon-circle">{ICON_MICROSCOPE}</div>
                    <h5>Topic Engine</h5>
                    <p>AI Gemini Pro</p>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <div class="flow-icon-circle">{ICON_CPU}</div>
                    <h5>Colab Engine</h5>
                    <p>GPU 4K Render</p>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <div class="flow-icon-circle">{ICON_CLOUD}</div>
                    <h5>Drive Storage</h5>
                    <p>Cloud Factory</p>
                </div>
                <div class="flow-arrow">➔</div>
                <div class="flow-node">
                    <div class="flow-icon-circle">{ICON_ROCKET}</div>
                    <h5>Auto Upload</h5>
                    <p>YouTube Studio</p>
                </div>
            </div>
        </div>
        
        <div class="cover-footer">
            <span>Diterbitkan oleh: <b>ZiyanCorp Publishing</b></span>
            <span>Versi Resmi: <b>v2.4 Production Standard</b></span>
        </div>
    </div>

    <!-- HALAMAN 2: BAB 1 - DENGAN ICON ILUSTRASI BULAT & WORKFLOW DIAGRAM -->
    <div class="page">
        <div class="chapter-tag">BAB 01 — ARSITEKTUR PABRIK KONTEN</div>
        <h2>Membangun Jalur Pipa Produksi Tanpa Coding Manual</h2>
        
        <p>Banyak kreator pemula mengalami kegagalan karena terjebak dalam proses manual yang menguras tenaga. Sistem ZiyanCorp membalikkan paradigma tersebut dengan memanfaatkan infrastruktur Cloud dan kecerdasan buatan.</p>
        
        <!-- 4 FEATURE CARDS DENGAN ICON ILUSTRASI LINGKARAN -->
        <div class="feature-grid">
            <div class="feature-card">
                <div class="icon-badge-blue">
                    {ICON_MICROSCOPE}
                </div>
                <div class="feature-card-content">
                    <h4>Riset Ide & Hook 3 Detik</h4>
                    <p>Gemini AI membedah subjek unik dengan daya tarik emosional tinggi dan meracik hook pembuka.</p>
                </div>
            </div>
            
            <div class="feature-card">
                <div class="icon-badge-sky">
                    {ICON_CPU}
                </div>
                <div class="feature-card-content">
                    <h4>Komputasi Cloud GPU</h4>
                    <p>Proses pemotongan video 4K, audio ducking, dan subtitle kotak kuning diproses di server Colab.</p>
                </div>
            </div>
            
            <div class="feature-card">
                <div class="icon-badge-indigo">
                    {ICON_CLOUD}
                </div>
                <div class="feature-card-content">
                    <h4>Penyimpanan Terpusat</h4>
                    <p>Semua master video matang otomatis disinkronkan ke folder Google Drive tanpa beban harddisk lokal.</p>
                </div>
            </div>
            
            <div class="feature-card">
                <div class="icon-badge-teal">
                    {ICON_ROCKET}
                </div>
                <div class="feature-card-content">
                    <h4>Auto-Schedule YouTube</h4>
                    <p>Video diunggah dan dijadwalkan tayang tepat pada jam puncak penonton internasional (US/Global).</p>
                </div>
            </div>
        </div>
        
        <!-- ILUSTRASI WORKFLOW HORIZONTAL -->
        <div class="workflow-box">
            <div class="workflow-header">
                <h5>{ICON_TARGET} Alur Kerja Produksi Otomatis (End-to-End)</h5>
                <span class="pill-badge">Zero Human Touch</span>
            </div>
            <div class="workflow-steps">
                <div class="step-item">
                    <div class="step-icon-sm">{ICON_MICROSCOPE}</div>
                    <h6>1. Generate</h6>
                    <span>Naskah & Prompt</span>
                </div>
                <div class="step-arrow">{ICON_ARROW_RIGHT}</div>
                <div class="step-item">
                    <div class="step-icon-sm">{ICON_CPU}</div>
                    <h6>2. Render 4K</h6>
                    <span>Video & Audio</span>
                </div>
                <div class="step-arrow">{ICON_ARROW_RIGHT}</div>
                <div class="step-item">
                    <div class="step-icon-sm">{ICON_CLOUD}</div>
                    <h6>3. Archive</h6>
                    <span>Google Drive</span>
                </div>
                <div class="step-arrow">{ICON_ARROW_RIGHT}</div>
                <div class="step-item">
                    <div class="step-icon-sm">{ICON_ROCKET}</div>
                    <h6>4. Publish</h6>
                    <span>YouTube Shorts</span>
                </div>
            </div>
        </div>
        
        <div class="callout-box">
            <div class="callout-icon">{ICON_LIGHTBULB}</div>
            <div>
                <h5>Kunci Efisiensi ZiyanCorp:</h5>
                <p>Laptop Anda hanya berfungsi sebagai pengirim komando (dispatcher). Seluruh beban komputasi berat 100% dipindahkan ke cloud server Google.</p>
            </div>
        </div>
        
        <div class="page-footer">
            <span>Pabrik Konten AI 24 Jam</span>
            <span>Halaman 01</span>
        </div>
    </div>

    <!-- HALAMAN 3: BAB 2 - DENGAN KPI METRICS & CHECKLIST ILUSTRASI -->
    <div class="page">
        <div class="chapter-tag">BAB 02 — FORMULA RETENSI ALGORITMA</div>
        <h2>Menembus 100 Juta Views dengan Retention Engineering</h2>
        
        <p>Algoritma YouTube Shorts tidak menyukai keberuntungan. Algoritma adalah mesin matematika presisi yang hanya mengevaluasi dua indikator utama penonton.</p>
        
        <!-- KPI METRIC CARDS -->
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-number">>85%</div>
                <div class="kpi-label">Target VVSA</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-number">>110%</div>
                <div class="kpi-label">Target APV (Loop)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-number">3x/Hari</div>
                <div class="kpi-label">Frekuensi Organik</div>
            </div>
        </div>
        
        <p>Untuk mencapai metrik tersebut secara konsisten, setiap video yang diproduksi oleh sistem wajib memenuhi 4 pilar psikologi penonton:</p>
        
        <div class="feature-grid" style="margin-top: 15px;">
            <div class="feature-card">
                <div class="icon-badge-blue">
                    {ICON_SHIELD}
                </div>
                <div class="feature-card-content">
                    <h4>The Cognitive Gap</h4>
                    <p>Membuka video dengan fakta yang mematahkan asumsi umum di 3 detik pertama.</p>
                </div>
            </div>
            
            <div class="feature-card">
                <div class="icon-badge-sky">
                    {ICON_TARGET}
                </div>
                <div class="feature-card-content">
                    <h4>Anthropomorphism</h4>
                    <p>Menghubungkan perilaku satwa dengan emosi manusiawi (kesepian, cinta, pengorbanan).</p>
                </div>
            </div>
            
            <div class="feature-card">
                <div class="icon-badge-indigo">
                    {ICON_LIGHTBULB}
                </div>
                <div class="feature-card-content">
                    <h4>Open Loop Hook</h4>
                    <p>Menahan jawaban terbesar hingga detik ke-40 agar penonton tidak menggeser layar.</p>
                </div>
            </div>
            
            <div class="feature-card">
                <div class="icon-badge-teal">
                    {ICON_ROCKET}
                </div>
                <div class="feature-card-content">
                    <h4>Seamless Infinite Loop</h4>
                    <p>Kalimat penutup menyambung mulus ke kalimat pembuka untuk memicu pemutaran ulang.</p>
                </div>
            </div>
        </div>
        
        <div class="page-footer">
            <span>Pabrik Konten AI 24 Jam</span>
            <span>Halaman 02</span>
        </div>
    </div>

</body>
</html>
"""

out_html = ROOT / "Ebook_Icon_Illustration_Sample.html"
out_html.write_text(html_doc, encoding="utf-8")
print(f"✅ HTML E-Book Siap: {out_html}")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

out_pdf = ROOT / "Ebook_Icon_Illustration_Sample.pdf"
if os.path.exists(chrome_path):
    print("🖨️ 2. Mencetak ke PDF Kualitas Vektor...")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={out_pdf}",
        str(out_html)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ PDF Tercipta: {out_pdf} ({out_pdf.stat().st_size / 1024:.1f} KB)")

# 3. Upload to Google Drive
print("☁️ 3. Mengunggah ke Google Drive ZIYANCORP_AI_FACTORY...")
token_path = r'C:\Users\arija\ziyancorp\abangjal_archive_bot\token.json'
creds = Credentials.from_authorized_user_file(token_path)
service = build('drive', 'v3', credentials=creds)

res = service.files().list(q="name='ZIYANCORP_AI_FACTORY' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields='files(id, name)').execute()
folders = res.get('files', [])

if folders:
    folder_id = folders[0]['id']
    file_name = '00_CONTOH_EBOOK_ILUSTRASI_ICON_TECH.pdf'
    media = MediaFileUpload(str(out_pdf), mimetype='application/pdf')
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    # Check if exists to overwrite/update
    existing = service.files().list(q=f"name='{file_name}' and '{folder_id}' in parents and trashed=false", fields='files(id)').execute().get('files', [])
    for exf in existing:
        try:
            service.files().delete(fileId=exf['id']).execute()
        except Exception:
            pass
            
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name, webViewLink').execute()
    print("="*60)
    print("🎉 SUKSES BESAR! E-BOOK ILUSTRASI ICON SUDAH TERSEDIA DI GOOGLE DRIVE!")
    print(f"📄 File Name : {uploaded.get('name')}")
    print(f"🆔 File ID   : {uploaded.get('id')}")
    print(f"🔗 Link View : {uploaded.get('webViewLink')}")
    print("="*60)
