#!/usr/bin/env python3
"""
ZAS Deploy/Import Utility — Mengunggah workflow JSON lokal ke n8n instance dan mengaktifkannya.
"""
import os
import json
from pathlib import Path
from n8n_client import N8NClient

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent / "workflows"

def deploy_workflows():
    client = N8NClient()
    print("Menghubungi n8n instance untuk deployment...")
    health = client.health_check()
    if health.get("status") != "ok":
        print(f"Peringatan: Server n8n belum aktif atau error: {health}")
        print("Silakan jalankan n8n instance terlebih dahulu (misal: via docker atau npx n8n).")
        return

    json_files = list(WORKFLOWS_DIR.glob("*.json"))
    print(f"Menemukan {len(json_files)} file workflow siap deploy di {WORKFLOWS_DIR}.")

    for jf in json_files:
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
            print(f"\nMengunggah workflow: {data.get('name', jf.stem)}...")
            res = client.create_workflow(data)
            new_id = res.get("id")
            print(f"[SUKSES] Workflow terpasang dengan ID: {new_id}")
        except Exception as e:
            print(f"[GAGAL] Gagal mengunggah {jf.name}: {e}")

if __name__ == "__main__":
    deploy_workflows()
