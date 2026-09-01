#!/usr/bin/env python3
"""
ZiyanCorp — Lynk.id Automated Product Sync Engine
Fetches live products, pricing, thumbnails, and direct links from https://lynk.id/yang_mulia
Updates src/data/products.json automatically
"""
import os
import sys
import json
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

STORE_URL = "https://lynk.id/yang_mulia"
ROOT = Path(__file__).parent
OUTPUT_JSON = ROOT / "src" / "data" / "products.json"
OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

def sync_products():
    print(f"Connecting to Lynk.id Store: {STORE_URL} ...")
    try:
        r = requests.get(STORE_URL, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"Failed to fetch store: HTTP {r.status_code}")
            return False
        
        soup = BeautifulSoup(r.text, "html.parser")
        products = []
        
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/yang_mulia/" in href:
                slug = href.split("/")[-1]
                if slug in ("terms_of_service", "privacy_policy", "refund_policy", "shipping_policy", "login"):
                    continue
                if len(slug) < 5:
                    continue
                
                # Title
                title_p = a.find("p", class_=re.compile("filter", re.I)) or a.find("p")
                title = title_p.get_text(strip=True) if title_p else "Produk Digital"
                
                # Price
                price_span = a.find("span", class_=re.compile("price", re.I)) or a.find(text=re.compile(r"IDR|Free|Rp", re.I))
                price_text = price_span.get_text(strip=True) if hasattr(price_span, 'get_text') else str(price_span or "Rp 0")
                if "IDR" in price_text:
                    clean_price = price_text.replace("IDR", "Rp").strip()
                elif "Free" in price_text or "Gratis" in price_text:
                    clean_price = "Gratis (Free)"
                else:
                    clean_price = price_text
                
                # Image
                img_tag = a.find("img")
                img_url = img_tag.get("src") if img_tag else ""
                if img_url and "?" in img_url:
                    img_url = img_url.split("?")[0]
                
                # Description mapping / fallback
                desc = ""
                if "Mesin Pencetak Uang" in title:
                    desc = "Panduan lengkap membangun channel YouTube otomatis (Faceless) yang menghasilkan pasif income konsisten tanpa perlu rekam wajah atau coding."
                    color = "from-crimson-600 to-rose-600"
                    glow = "from-crimson-600 via-rose-500 to-amber-500"
                    badge = "Best Seller"
                    btn = "Beli Sekarang"
                elif "Cetak Biru" in title or "GRATIS" in title:
                    desc = "Blueprint rahasia membuat video animasi dan karakter AI fotorealistis yang bergerak natural, konsisten, ekspresif, dan anti-kaku."
                    color = "from-emerald-600 to-teal-600"
                    glow = "from-emerald-500 via-teal-400 to-cyan-500"
                    badge = "Free Access"
                    btn = "Ambil Gratis"
                elif "Hook" in title or "Affiliate" in title:
                    desc = "Kumpulan formula 100+ hook viral 3 detik pertama terbukti ampuh mendongkrak retensi penonton dan omset affiliate TikTok & Shopee."
                    color = "from-indigo-600 to-violet-600"
                    glow = "from-indigo-500 via-purple-500 to-rose-500"
                    badge = "Hot Item"
                    btn = "Dapatkan Sekarang"
                else:
                    desc = "Aset digital eksklusif dari ZiyanCorp untuk memaksimalkan produktivitas dan monetisasi konten AI Anda."
                    color = "from-violet-600 to-cyan-600"
                    glow = "from-violet-500 via-cyan-400 to-rose-500"
                    badge = "Digital Asset"
                    btn = "Beli di Lynk.id"

                is_free = "Free" in clean_price or "Gratis" in clean_price
                full_url = f"https://lynk.id/yang_mulia/{slug}" if not href.startswith("http") else href
                
                products.append({
                    "id": slug,
                    "title": title,
                    "description": desc,
                    "price": clean_price,
                    "status": "available",
                    "is_free": is_free,
                    "url": full_url,
                    "image": img_url,
                    "badge": badge,
                    "color": color,
                    "border_glow": glow,
                    "btn_label": btn
                })
        
        # Deduplicate
        seen = set()
        unique_prods = []
        for p in products:
            if p["id"] not in seen:
                seen.add(p["id"])
                unique_prods.append(p)
        
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f_out:
            json.dump(unique_prods, f_out, indent=2, ensure_ascii=False)
            
        print(f"✅ Successfully synced {len(unique_prods)} products to {OUTPUT_JSON}")
        return True
    except Exception as e:
        print(f"❌ Error syncing with Lynk.id: {e}")
        return False

if __name__ == "__main__":
    sync_products()
