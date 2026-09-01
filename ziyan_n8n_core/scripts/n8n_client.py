#!/usr/bin/env python3
"""
ZAS (Ziyan Automation Systems) - n8n Python Client Wrapper
Menyediakan antarmuka Python untuk mengelola dan memonitor n8n instance secara terprogram.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
load_dotenv(CONFIG_DIR / ".env")


class N8NClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("N8N_INSTANCE_URL", "http://localhost:5678")).rstrip("/")
        self.api_key = api_key or os.environ.get("N8N_API_KEY", "")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.api_key:
            self.headers["X-N8N-API-KEY"] = self.api_key

    def health_check(self) -> Dict[str, Any]:
        """Periksa konektivitas n8n instance."""
        try:
            r = requests.get(f"{self.base_url}/healthz", timeout=10)
            return {"status": "ok" if r.status_code == 200 else "degraded", "code": r.status_code}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_workflows(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """Ambil daftar seluruh workflow yang terdaftar di n8n."""
        params = {"active": "true"} if active_only else {}
        r = requests.get(f"{self.base_url}/api/v1/workflows", headers=self.headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("data", [])

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Ambil detail lengkap 1 workflow JSON berdasarkan ID."""
        r = requests.get(f"{self.base_url}/api/v1/workflows/{workflow_id}", headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.json().get("data", {})

    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Unggah dan buat workflow baru ke n8n instance."""
        r = requests.post(f"{self.base_url}/api/v1/workflows", headers=self.headers, json=workflow_data, timeout=30)
        r.raise_for_status()
        return r.json().get("data", {})

    def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Aktifkan trigger otomatis workflow."""
        r = requests.post(f"{self.base_url}/api/v1/workflows/{workflow_id}/activate", headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.json().get("data", {})

    def trigger_webhook(self, path: str, payload: Dict[str, Any], is_test: bool = False) -> Dict[str, Any]:
        """Kirim trigger webhook HTTP ke n8n workflow."""
        prefix = "webhook-test" if is_test else "webhook"
        url = f"{self.base_url}/{prefix}/{path.lstrip('/')}"
        r = requests.post(url, json=payload, timeout=60)
        return {"status_code": r.status_code, "response": r.text}


if __name__ == "__main__":
    client = N8NClient()
    print("Memeriksa status n8n...")
    print(client.health_check())
