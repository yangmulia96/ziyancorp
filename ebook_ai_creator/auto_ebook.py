"""
ZiyanCorp Master E-Book Generator - Official 2026 Iconographic Edition
Generates premium tech-illustrated ebooks with SVG icons, architecture diagrams,
step-by-step workflow boxes, KPI cards, and auto-uploads to Google Drive.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
import json
import markdown
import subprocess
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).parent
load_dotenv(ROOT.parent / "arsip_celine_aurel" / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = "AQ.Ab8RN6Jh-jeCGKc3YTcSuVsaHUrVonnc4mUeJGqvAtbmGSd9mQ"

client = genai.Client(api_key=GEMINI_API_KEY)

# --- SVG ICONS LIBRARY ---
ICONS = {
    "microscope": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 22h18"/><path d="m14 22 1-4H9l1 4"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="m12 6 3-3 3 3-3 3Z"/></svg>""",
    "cpu": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>""",
    "cloud": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>""",
    "rocket": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>""",
    "shield": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>""",
    "target": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "lightbulb": """<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>""",
    "arrow_right": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>"""
}

def generate_book_content(topic: str) -> dict:
    """Generate structured book content with Gemini AI."""
    print(f"🤖 AI sedang merancang blueprint dan konten untuk: '{topic}'...")
    prompt = f"""Kamu adalah penulis E-Book profesional kelas dunia dari ZiyanCorp Publishing.
Tugasmu: Tulis naskah E-Book komprehensif, padat, dan aplikatif tentang topik: '{topic}'.

Format gaya bahasa:
- Bahasa Indonesia yang cerdas, asik, berbobot tinggi, dan profesional.
- Mindset: Pembaca sebagai Sutradara/Pemilik Bisnis, AI dan automasi sebagai armada pekerja.

Struktur Output JSON (HANYA kembalikan JSON valid tanpa markdown block):
{{
  "title": "{topic}",
  "subtitle": "Panduan Komprehensif & Blueprint Eksekusi ZiyanCorp",
  "author": "ZiyanCorp Publishing",
  "edition": "Official 2026 Iconographic Blueprint",
  "introduction": "Kata pengantar 3-4 paragraf yang menggugah, membuka wawasan pembaca tentang pentingnya topik ini.",
  "pipeline_steps": [
    {{"name": "Research", "sub": "Data & Insight"}},
    {{"name": "Execution", "sub": "Cloud Engine"}},
    {{"name": "Storage", "sub": "Central Archive"}},
    {{"name": "Distribution", "sub": "Auto Release"}}
  ],
  "chapters": [
    {{
      "chapter_num": "01",
      "tag": "BAB 01 — ARSITEKTUR & MINDSET",
      "title": "Judul Bab 1",
      "summary": "Ringkasan konsep bab 1...",
      "feature_cards": [
        {{"icon": "microscope", "title": "Poin 1", "desc": "Deskripsi singkat 2 baris."}},
        {{"icon": "cpu", "title": "Poin 2", "desc": "Deskripsi singkat 2 baris."}},
        {{"icon": "cloud", "title": "Poin 3", "desc": "Deskripsi singkat 2 baris."}},
        {{"icon": "rocket", "title": "Poin 4", "desc": "Deskripsi singkat 2 baris."}}
      ],
      "workflow_title": "Alur Kerja Eksekusi Bab 1",
      "workflow_steps": [
        {{"icon": "microscope", "step": "1. Analisis", "desc": "Riset Data"}},
        {{"icon": "cpu", "step": "2. Proses", "desc": "Automasi"}},
        {{"icon": "cloud", "step": "3. Simpan", "desc": "Database"}},
        {{"icon": "rocket", "step": "4. Luncurkan", "desc": "Hasil Akhir"}}
      ],
      "callout_title": "Kunci Penting Bab 1",
      "callout_text": "Pesan inti penting yang harus diingat pembaca."
    }},
    {{
      "chapter_num": "02",
      "tag": "BAB 02 — STRATEGI & METRIK HASIL",
      "title": "Judul Bab 2",
      "summary": "Ringkasan konsep bab 2...",
      "kpis": [
        {{"number": "85%+", "label": "Target Retensi"}},
        {{"number": "10x", "label": "Efisiensi Waktu"}},
        {{"number": "100%", "label": "Autopilot System"}}
      ],
      "feature_cards": [
        {{"icon": "shield", "title": "Pilar 1", "desc": "Deskripsi singkat 2 baris."}},
        {{"icon": "target", "title": "Pilar 2", "desc": "Deskripsi singkat 2 baris."}},
        {{"icon": "lightbulb", "title": "Pilar 3", "desc": "Deskripsi singkat 2 baris."}},
        {{"icon": "rocket", "title": "Pilar 4", "desc": "Deskripsi singkat 2 baris."}}
      ],
      "callout_title": "Formula Sukses:",
      "callout_text": "Strategi actionable yang langsung bisa dipraktekkan pembaca."
    }}
  ]
}}"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    return json.loads(raw)

def build_html_document(data: dict) -> str:
    """Build ultra-clean Tech Iconographic HTML E-Book."""
    title = data.get("title", "ZiyanCorp Blueprint")
    subtitle = data.get("subtitle", "Panduan Eksekusi Otomatis")
    author = data.get("author", "ZiyanCorp Publishing")
    edition = data.get("edition", "Official 2026 Edition")
    intro = data.get("introduction", "")
    pipeline = data.get("pipeline_steps", [])
    chapters = data.get("chapters", [])

    # Build Cover Pipeline Nodes
    pipeline_html = ""
    for i, p in enumerate(pipeline):
        icon_key = ["microscope", "cpu", "cloud", "rocket"][i % 4]
        icon_svg = ICONS.get(icon_key, ICONS["cpu"])
        pipeline_html += f"""
        <div class="flow-node">
            <div class="flow-icon-circle">{icon_svg}</div>
            <h5>{p.get('name')}</h5>
            <p>{p.get('sub')}</p>
        </div>
        """
        if i < len(pipeline) - 1:
            pipeline_html += """<div class="flow-arrow">➔</div>"""

    # Build Chapters HTML
    chapters_html = ""
    for idx, ch in enumerate(chapters):
        page_num = f"{idx + 1:02d}"
        ch_tag = ch.get("tag", f"BAB {idx+1}")
        ch_title = ch.get("title", "")
        ch_summary = ch.get("summary", "")
        
        # Feature cards
        cards_html = ""
        badge_colors = ["blue", "sky", "indigo", "teal"]
        for ci, card in enumerate(ch.get("feature_cards", [])):
            c_icon = ICONS.get(card.get("icon", "cpu"), ICONS["cpu"])
            c_color = badge_colors[ci % len(badge_colors)]
            cards_html += f"""
            <div class="feature-card">
                <div class="icon-badge-{c_color}">
                    {c_icon}
                </div>
                <div class="feature-card-content">
                    <h4>{card.get('title')}</h4>
                    <p>{card.get('desc')}</p>
                </div>
            </div>
            """

        # Optional Workflow
        workflow_html = ""
        if ch.get("workflow_steps"):
            steps_html = ""
            for si, step in enumerate(ch.get("workflow_steps", [])):
                s_icon = ICONS.get(step.get("icon", "cpu"), ICONS["cpu"])
                steps_html += f"""
                <div class="step-item">
                    <div class="step-icon-sm">{s_icon}</div>
                    <h6>{step.get('step')}</h6>
                    <span>{step.get('desc')}</span>
                </div>
                """
                if si < len(ch.get("workflow_steps")) - 1:
                    steps_html += f"""<div class="step-arrow">{ICONS['arrow_right']}</div>"""
            
            workflow_html = f"""
            <div class="workflow-box">
                <div class="workflow-header">
                    <h5>{ICONS['target']} {ch.get('workflow_title', 'Alur Kerja Sistem')}</h5>
                    <span class="pill-badge">Standard Workflow</span>
                </div>
                <div class="workflow-steps">
                    {steps_html}
                </div>
            </div>
            """

        # Optional KPIs
        kpi_html = ""
        if ch.get("kpis"):
            kpi_cards = ""
            for k in ch.get("kpis", []):
                kpi_cards += f"""
                <div class="kpi-card">
                    <div class="kpi-number">{k.get('number')}</div>
                    <div class="kpi-label">{k.get('label')}</div>
                </div>
                """
            kpi_html = f"""<div class="kpi-row">{kpi_cards}</div>"""

        # Callout Box
        callout_html = ""
        if ch.get("callout_title"):
            callout_html = f"""
            <div class="callout-box">
                <div class="callout-icon">{ICONS['lightbulb']}</div>
                <div>
                    <h5>{ch.get('callout_title')}</h5>
                    <p>{ch.get('callout_text')}</p>
                </div>
            </div>
            """

        chapters_html += f"""
        <div class="page">
            <div class="chapter-tag">{ch_tag}</div>
            <h2>{ch_title}</h2>
            <p>{ch_summary}</p>
            {kpi_html}
            <div class="feature-grid">{cards_html}</div>
            {workflow_html}
            {callout_html}
            <div class="page-footer">
                <span>{title}</span>
                <span>Halaman {page_num}</span>
            </div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
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
            font-size: 46px;
            font-weight: 900;
            line-height: 1.18;
            margin: 22px 0 12px 0;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: -0.5px;
        }}
        .cover-subtitle {{
            font-size: 17.5px;
            color: #94a3b8;
            line-height: 1.6;
            max-width: 580px;
            margin-bottom: 25px;
        }}
        .cover-diagram {{
            width: 100%;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 22px;
            backdrop-filter: blur(12px);
            margin: 15px 0;
        }}
        .diagram-title {{
            font-size: 12px;
            font-weight: 800;
            color: #94a3b8;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 16px;
            text-align: center;
        }}
        .cover-flow {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        }}
        .flow-node {{
            flex: 1;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 14px;
            padding: 14px 10px;
            text-align: center;
        }}
        .flow-icon-circle {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #2563eb, #0284c7);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 8px auto;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }}
        .flow-node h5 {{ font-size: 12.5px; font-weight: 700; color: #f8fafc; margin-bottom: 2px; }}
        .flow-node p {{ font-size: 10.5px; color: #94a3b8; }}
        .flow-arrow {{ color: #38bdf8; font-size: 18px; font-weight: 900; }}
        .cover-footer {{
            width: 100%;
            border-top: 1px solid rgba(255, 255, 255, 0.12);
            padding-top: 18px;
            display: flex;
            justify-content: space-between;
            font-size: 12.5px;
            color: #94a3b8;
        }}
        .chapter-tag {{
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #2563eb;
            margin-bottom: 8px;
        }}
        h2 {{
            font-size: 28px;
            font-weight: 900;
            color: #0f172a;
            line-height: 1.25;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
        }}
        p {{
            font-size: 14.5px;
            line-height: 1.75;
            color: #475569;
            margin-bottom: 16px;
        }}
        .feature-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
            margin: 20px 0;
        }}
        .feature-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 15px;
            padding: 18px;
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }}
        .icon-badge-blue {{
            flex-shrink: 0; width: 48px; height: 48px; border-radius: 50%;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            display: flex; align-items: center; justify-content: center; color: #ffffff;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
        }}
        .icon-badge-sky {{
            flex-shrink: 0; width: 48px; height: 48px; border-radius: 50%;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            display: flex; align-items: center; justify-content: center; color: #ffffff;
            box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
        }}
        .icon-badge-indigo {{
            flex-shrink: 0; width: 48px; height: 48px; border-radius: 50%;
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
            display: flex; align-items: center; justify-content: center; color: #ffffff;
            box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
        }}
        .icon-badge-teal {{
            flex-shrink: 0; width: 48px; height: 48px; border-radius: 50%;
            background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
            display: flex; align-items: center; justify-content: center; color: #ffffff;
            box-shadow: 0 4px 10px rgba(13, 148, 136, 0.25);
        }}
        .feature-card-content h4 {{ font-size: 15px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }}
        .feature-card-content p {{ font-size: 13px; line-height: 1.5; color: #64748b; margin-bottom: 0; }}
        .workflow-box {{
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 16px;
            padding: 18px;
            margin: 22px 0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }}
        .workflow-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e2e8f0;
        }}
        .workflow-header h5 {{
            font-size: 13.5px;
            font-weight: 800;
            color: #1e293b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .pill-badge {{
            background: #dbeafe;
            color: #1d4ed8;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 10.5px;
            font-weight: 700;
        }}
        .workflow-steps {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
        }}
        .step-item {{
            flex: 1;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 11px;
            padding: 12px 8px;
            text-align: center;
        }}
        .step-icon-sm {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            background: #eff6ff;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 6px auto;
        }}
        .step-item h6 {{ font-size: 11.5px; font-weight: 800; color: #0f172a; margin-bottom: 2px; }}
        .step-item span {{ font-size: 10px; color: #64748b; }}
        .step-arrow {{ color: #94a3b8; display: flex; align-items: center; }}
        .callout-box {{
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            border-radius: 12px;
            padding: 16px 18px;
            margin: 20px 0;
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }}
        .callout-icon {{ color: #2563eb; flex-shrink: 0; margin-top: 2px; }}
        .callout-box h5 {{ font-size: 14.5px; font-weight: 800; color: #1e40af; margin-bottom: 3px; }}
        .callout-box p {{ font-size: 13px; line-height: 1.55; color: #1e3a8a; margin-bottom: 0; }}
        .kpi-row {{ display: flex; gap: 12px; margin: 18px 0; }}
        .kpi-card {{
            flex: 1;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 13px;
            padding: 14px;
            text-align: center;
        }}
        .kpi-number {{ font-size: 26px; font-weight: 900; color: #2563eb; line-height: 1.1; margin-bottom: 3px; }}
        .kpi-label {{ font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; }}
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
    <!-- COVER -->
    <div class="page cover">
        <div>
            <div class="brand-badge">
                {ICONS['cpu']} {author} • {edition}
            </div>
            <h1>{title}</h1>
            <p class="cover-subtitle">{subtitle}</p>
        </div>
        
        <div class="cover-diagram">
            <div class="diagram-title">PIPELINE ARSITEKTUR SISTEM</div>
            <div class="cover-flow">
                {pipeline_html}
            </div>
        </div>
        
        <div class="cover-footer">
            <span>Penerbit: <b>{author}</b></span>
            <span>Standard: <b>Production Ready</b></span>
        </div>
    </div>

    <!-- CHAPTERS -->
    {chapters_html}
</body>
</html>
"""
    return full_html

def create_master_ebook(topic: str) -> dict:
    """End-to-end master ebook pipeline."""
    data = generate_book_content(topic)
    html_content = build_html_document(data)
    
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', topic)[:40]
    out_html = ROOT / f"{safe_name}.html"
    out_pdf = ROOT / f"{safe_name}.pdf"
    
    out_html.write_text(html_content, encoding="utf-8")
    print(f"✅ HTML Generated: {out_html.name}")
    
    # Compile to PDF
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        
    if os.path.exists(chrome_path):
        print("🖨️ Mencetak ke PDF Vektor Tajam...")
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={out_pdf}",
            str(out_html)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"🎉 PDF Siap: {out_pdf.name} ({out_pdf.stat().st_size / 1024:.1f} KB)")
        
        # Upload to Google Drive
        try:
            token_path = ROOT.parent / "abangjal_archive_bot" / "token.json"
            creds = Credentials.from_authorized_user_file(str(token_path))
            service = build('drive', 'v3', credentials=creds)
            
            res = service.files().list(q="name='ZIYANCORP_AI_FACTORY' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields='files(id, name)').execute()
            folders = res.get('files', [])
            if folders:
                folder_id = folders[0]['id']
                file_metadata = {'name': f"{safe_name}.pdf", 'parents': [folder_id]}
                media = MediaFileUpload(str(out_pdf), mimetype='application/pdf')
                uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name, webViewLink').execute()
                print(f"☁️ Uploaded to Drive: {uploaded.get('webViewLink')}")
                return {"pdf_path": str(out_pdf), "drive_link": uploaded.get('webViewLink')}
        except Exception as e:
            print(f"⚠️ Drive upload warning: {e}")
            
    return {"pdf_path": str(out_pdf), "drive_link": None}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "Sistem Automasi YouTube Shorts 100M Views"
    create_master_ebook(topic)
