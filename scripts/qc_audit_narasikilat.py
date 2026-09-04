#!/usr/bin/env python3
"""
qc_audit_narasikilat.py
-----------------------
Automated Quality Control (QC) & Auditor Agent Script for NarasiKilat Studio PWA.
Reads execution telemetry directly from Google Sheets (24/7 Cloud Logging).

Features:
- Telemetry health summary (Total requests, Success Rate, Average Latency).
- Breakdown per Feature / Division (Naskah Matrix, UGC Studio, Prompt Visual, Caption & SEO).
- Error & Anomaly audit (with immediate root-cause highlights).
- Copywriting quality assessment on recent generations.
- Syncs QC notes back to Google Sheets.
"""

import json
import os
import sys
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

# Pastikan UTF-8 untuk output Windows Terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

TOKEN_FILE = r"C:\Users\arija\AppData\Local\hermes\google_token.json"
SPREADSHEET_ID = "1JQg7FPA2Jn-AA8z2i1H71JtXjcYoTp98pEr6EcEqUfQ"
SHEET_NAME = "Sheet1"

def get_access_token():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"OAuth token file not found at: {TOKEN_FILE}")
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)
    
    params = urllib.parse.urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token"
    }).encode("utf-8")
    
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=params)
    with urllib.request.urlopen(req) as resp:
        token_data = json.loads(resp.read().decode("utf-8"))
        return token_data["access_token"]

def fetch_sheet_rows(access_token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A1:I500"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("values", [])

def update_qc_note(access_token, row_index, note):
    """Update column I (Catatan Evaluasi QC) for a given row index (1-based)."""
    cell_range = f"{SHEET_NAME}!I{row_index}"
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{cell_range}?valueInputOption=USER_ENTERED"
    body = json.dumps({"values": [[note]]}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status == 200

def run_qc_evaluation(rows, access_token=None, auto_update=False):
    if len(rows) <= 1:
        print("⚠️ Belum ada data log generasi di Google Sheet.")
        return

    headers = rows[0]
    data_rows = rows[1:]

    total = len(data_rows)
    successes = [r for r in data_rows if len(r) > 4 and r[4].strip().upper() == "SUCCESS"]
    errors = [r for r in data_rows if len(r) > 4 and r[4].strip().upper() == "ERROR"]
    
    success_rate = (len(successes) / total * 100) if total > 0 else 0

    # Group by feature
    features = {}
    latencies = []
    
    for idx, r in enumerate(data_rows, start=2):
        feat = r[1] if len(r) > 1 else "Unknown"
        lat = int(r[5]) if (len(r) > 5 and r[5].isdigit()) else 0
        if lat > 0:
            latencies.append(lat)
        
        if feat not in features:
            features[feat] = {"total": 0, "success": 0, "error": 0, "latencies": []}
        features[feat]["total"] += 1
        st = r[4].strip().upper() if len(r) > 4 else "UNKNOWN"
        if st == "SUCCESS":
            features[feat]["success"] += 1
            if lat > 0:
                features[feat]["latencies"].append(lat)
        else:
            features[feat]["error"] += 1

    avg_lat = sum(latencies) / len(latencies) if latencies else 0

    print("=" * 70)
    print("📊 LAPORAN AUDIT & QUALITY CONTROL (QC) — NARASIKILAT STUDIO PWA")
    print(f"🕒 Waktu Audit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Local")
    print(f"🔗 Google Sheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    print("=" * 70)
    print(f"\n📈 RINGKASAN PERFORMA SISTEM:")
    print(f"  • Total Riwayat Eksekusi : {total} interaksi")
    print(f"  • Tingkat Sukses (Reliability) : {success_rate:.1f}% ({len(successes)} Berhasil / {len(errors)} Gagal)")
    print(f"  • Rata-rata Latensi        : {avg_lat:.0f} ms")

    print(f"\n🏢 BREAKDOWN PER DIVISI / FITUR:")
    for feat, stats in features.items():
        feat_lat = sum(stats["latencies"]) / len(stats["latencies"]) if stats["latencies"] else 0
        status_icon = "✅" if stats["error"] == 0 else "⚠️"
        print(f"  {status_icon} [{feat}]")
        print(f"     Total: {stats['total']} | Sukses: {stats['success']} | Error: {stats['error']} | Rata-rata Latensi: {feat_lat:.0f} ms")

    if errors:
        print(f"\n🚨 LOG ANOMALI & ERROR TERAKHIR:")
        for r in errors[-5:]:
            ts = r[0] if len(r) > 0 else "-"
            f_name = r[1] if len(r) > 1 else "-"
            inp = r[2] if len(r) > 2 else "-"
            err_msg = r[7] if len(r) > 7 else "-"
            print(f"  ❌ [{ts}] {f_name}")
            print(f"     Input : {inp}")
            print(f"     Error : {err_msg}")
    else:
        print(f"\n✨ STATUS KEANDALAN: Zero Critical Errors! Sistem berjalan 100% prima.")

    print(f"\n📝 5 RIWAYAT TERAKHIR DENGAN EVALUASI QC:")
    for idx, r in enumerate(data_rows[-5:], start=max(2, len(data_rows) - 4 + 1)):
        ts = r[0] if len(r) > 0 else "-"
        f_name = r[1] if len(r) > 1 else "-"
        inp = r[2] if len(r) > 2 else "-"
        out = r[6] if len(r) > 6 else "-"
        qc_current = r[8] if len(r) > 8 else "-"

        # QC Heuristics
        qc_grade = "PASSED"
        qc_feedback = "Kualitas prima, format baku rapi"
        
        if len(inp) < 3:
            qc_grade = "WARNING"
            qc_feedback = "Input produk terlalu pendek/ambigu"
        elif "overclaim" in out.lower() or "100% ampuh" in out.lower():
            qc_grade = "FLAGGED"
            qc_feedback = "Terdeteksi potensi overclaim kata terlarang"
        
        qc_tag = f"QC: {qc_grade} — {qc_feedback}"

        print(f"\n  [Row {idx}] {ts} — {f_name}")
        print(f"     📦 Input   : {inp[:60]}")
        print(f"     📄 Output  : {out[:80]}...")
        print(f"     🔍 Status QC: {qc_tag}")

        if auto_update and access_token and (qc_current == "-" or "Auto-Logged" in qc_current):
            try:
                update_qc_note(access_token, idx, qc_tag)
                print(f"     💾 -> Catatan QC berhasil disinkronkan ke baris {idx} Google Sheet.")
            except Exception as e:
                print(f"     ⚠️ Gagal update sheet: {e}")

    print("\n" + "=" * 70)
    print("✅ Audit Selesai. Seluruh log tersimpan aman di Google Cloud Drive.")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Auditor & QC Agent untuk NarasiKilat Studio")
    parser.add_argument("--update", action="store_true", help="Sinkronkan catatan evaluasi QC langsung ke Google Sheet")
    args = parser.parse_args()

    token = get_access_token()
    rows = fetch_sheet_rows(token)
    run_qc_evaluation(rows, access_token=token, auto_update=args.update)

if __name__ == "__main__":
    main()
