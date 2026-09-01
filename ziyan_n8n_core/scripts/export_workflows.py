#!/usr/bin/env python3
"""
ZAS Export Utility — Mengekspor seluruh workflow aktif dari n8n instance ke file JSON lokal.
"""
import os
import json
from pathlib import Path
from n8n_client import N8NClient

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent / "workflows"
WORKFLOWS_DIR.mkdir(exist_ok=True)

def export_all():
    client = N8NClient()
    print("Menghubungi n8n instance...")
    health = client.health_check()
    if health.get("status") != "ok":
        print(f"Peringatan: Status server n8n: {health}")
    
    try:
        workflows = client.list_workflows()
        print(f"Ditemukan {len(workflows)} workflow di n8n instance.")
        for wf in workflows:
            wf_id = wf.get("id")
            wf_name = wf.get("name", "untitled").replace(" ", "_").replace("/", "-")
            wf_detail = client.get_workflow(wf_id)
            target_path = WORKFLOWS_DIR / f"{wf_id}_{wf_name}.json"
            target_path.write_text(json.dumps(wf_detail, indent=2), encoding="utf-8")
            print(f"[OK] Berhasil mengekspor: {target_path.name}")
        print("\nSelesai! Seluruh workflow berhasil dicadangkan ke lokal.")
    except Exception as e:
        print(f"Error saat mengekspor: {e}")

if __name__ == "__main__":
    export_all()
