#!/usr/bin/env python3
"""
AbangJal / Arijal Meutuwah Distributor - Orchestrator Distribusi Multi-Platform
Persona: AI Influencer "Arijal Meutuwah" (Pria / Affiliate TikTok / Lifestyle / Gadget)
Target Akun: Khusus Ekosistem Arijal Meutuwah (Bebas dari campur tangan akun Celine Aurel).
"""
import os, json, sys, re
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from dotenv import load_dotenv
import requests

ROOT = Path(r"C:\Users\arija\ziyancorp\abangjal_archive_bot")
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT))

from abangjal_bot.google_workspace import GoogleWorkspace
from abangjal_bot.config import Settings

NINE_ROUTER = "http://127.0.0.1:20128/v1/chat/completions"


def gen_caption(product: dict, persona: str = "Arijal Meutuwah") -> str:
    """Caption terstruktur untuk AI Influencer 'Arijal Meutuwah' (Shopee Affiliate).
    Format Baku:
    [Link Affiliate Shopee/Tautan Produk]

    [Deskripsi/Ulasan Produk yang Menarik & Persuasif]

    #HashtagRelevan #ArijalMeutuwah #ShopeeAffiliate
    """
    url = (product.get('shopee_url') or product.get('tiktok_url') or '').strip()
    title = product.get('title') or ''
    orig_desc = product.get('description') or ''
    
    # Bersihkan teks kotor harga
    clean_title = re.sub(r"dengan harga Rp[0-9.]+", "", title, flags=re.I).strip()
    clean_title = re.sub(r"\. Dapatkan di Shopee sekarang!.*", "", clean_title, flags=re.I).strip()
    clean_title = re.sub(r"^Cek\s+", "", clean_title, flags=re.I).strip()

    prompt = f"""Buat caption produk untuk akun AI influencer Pria "{persona}".
FORMAT WAJIB PERSIS (pisahkan tiap bagian dengan 1 baris kosong):
{url}

[1-2 kalimat deskripsi/ulasan produk yang menarik, meyakinkan & santai gaya {persona}, jelaskan keunggulan dan situasi pemakaian]

#RekomendasiProduk #ArijalMeutuwah #ShopeeAffiliate #OutfitPria #StyleHarian

ATURAN KETAT:
- Baris pertama HARUS link produk: {url}
- JANGAN menyebut nominal harga, diskon, atau angka rupiah.
- Jangan pakai gaya robotik.

Produk: {clean_title}"""

    # 1. Coba 9Router Local
    nine_key = os.environ.get("NINEROUTER_API_KEY") or os.environ.get("HERMES_CUSTOM_9ROUTER_API_KEY", "")
    if nine_key:
        try:
            headers = {"Authorization": f"Bearer {nine_key}", "Content-Type": "application/json"}
            r = requests.post(NINE_ROUTER, headers=headers, json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300, "temperature": 0.7, "stream": False
            }, timeout=15)
            if r.status_code == 200:
                data = r.json()
                content = data["choices"][0]["message"]["content"].strip()
                if content:
                    return content
        except Exception:
            pass

    # 2. Coba OpenRouter Gateway (:free)
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    if openrouter_key:
        try:
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ziyancorp.internal",
                "X-Title": "Ziyan Pipeline"
            }
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300, "temperature": 0.7
            }, timeout=20)
            if r.status_code == 200:
                data = r.json()
                content = data["choices"][0]["message"]["content"].strip()
                if content:
                    return content
        except Exception:
            pass

    # 3. Fallback Template Baku Arijal Meutuwah ($0 / Offline)
    desc_text = orig_desc if orig_desc else f"Rekomendasi terbaik hari ini: {clean_title}. Kualitas bahan mantap, potongan pas, dan siap upgrade penampilanmu!"
    return f"{url}\n\n{desc_text}\n\n#RekomendasiProduk #ArijalMeutuwah #ShopeeAffiliate #OutfitPria"


def post_telegram_channel(text: str, channel_id: str, bot_token: str) -> dict:
    if not channel_id or not bot_token:
        return {"status": "skipped", "reason": "no_token_or_channel"}
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": channel_id,
            "text": text,
            "disable_web_page_preview": False
        }, timeout=30).json()
        return {"status": "success" if r.get("ok") else "error", "response": r}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def post_youtube_arijal(title: str, description: str, video_path: str) -> dict:
    """Upload khusus channel YouTube Arijal Meutuwah menggunakan token_arijal.json."""
    token_file = ROOT / "token_arijal.json"
    if not token_file.exists():
        return {
            "status": "skipped",
            "reason": "token_arijal_not_found",
            "message": "Token YouTube Arijal Meutuwah (token_arijal.json) belum diotentikasi. Sistem menolak menggunakan token Celine demi menjaga isolasi channel."
        }
    
    if not video_path or not os.path.exists(video_path):
        return {"status": "skipped", "reason": "video_file_not_found"}
        
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        creds = Credentials.from_authorized_user_file(str(token_file))
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
        yt = build("youtube", "v3", credentials=creds)
        body = {
            "snippet": {
                "title": f"{title[:70]} #Shorts",
                "description": description,
                "tags": ["ArijalMeutuwah", "ShopeeAffiliate", "Shorts", "OutfitPria"],
                "categoryId": "26"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }
        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
        req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
        res = req.execute()
        vid_id = res.get("id")
        return {"status": "success", "platform": "youtube_arijal", "video_id": vid_id, "url": f"https://youtube.com/shorts/{vid_id}"}
    except Exception as e:
        return {"status": "error", "platform": "youtube_arijal", "error": str(e)}


def post_twitter_x_arijal(caption: str) -> dict:
    """Post tweet otomatis ke akun Twitter / X @Abangjal (Arijal Meutuwah)."""
    token_file = ROOT / "x_token_arijal.json"
    if not token_file.exists():
        return {"status": "skipped", "reason": "x_token_arijal_not_found"}
        
    try:
        data = json.loads(token_file.read_text(encoding="utf-8"))
        token = data.get("access_token")
        if not token:
            return {"status": "skipped", "reason": "no_x_access_token"}
            
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {"text": caption[:280]}
        r = requests.post("https://api.x.com/2/tweets", headers=headers, json=payload, timeout=30)
        res = r.json()
        if r.status_code in (200, 201) and "data" in res:
            tweet_id = res["data"]["id"]
            return {"status": "success", "platform": "twitter_x_arijal", "tweet_id": tweet_id, "url": f"https://x.com/Abangjal/status/{tweet_id}"}
        else:
            return {"status": "error", "platform": "twitter_x_arijal", "response": res, "http_status": r.status_code}
    except Exception as e:
        return {"status": "error", "platform": "twitter_x_arijal", "error": str(e)}


def distribute_to_platforms_arijal(product: dict, caption: str, targets: list = None, video_path: str = None) -> dict:
    """Distributor Khusus Persona Arijal Meutuwah - Target: YouTube Shorts Saja."""
    if targets is None:
        targets = ["youtube"]
    results = {}
    
    # YouTube Shorts Arijal Saja
    if "youtube" in targets or "all" in targets:
        yt_title = product.get("title") or ""
        import re
        yt_title = re.sub(r"dengan harga Rp[0-9.]+", "", yt_title, flags=re.I)
        yt_title = re.sub(r"\. Dapatkan di Shopee sekarang!.*", "", yt_title, flags=re.I)
        yt_title = re.sub(r"http\S+", "", yt_title).strip()
        if not yt_title or len(yt_title) < 3:
            yt_title = "Rekomendasi Fashion & Outfit Pria Keren 🔥"
        results["youtube"] = post_youtube_arijal(yt_title, caption, video_path)
        
    return results



if __name__ == "__main__":
    print("=== Distributor Arijal Meutuwah (Strict Isolation Active) ===")
    test_prod = {
        "title": "Classic Henley Fitted T-Shirt",
        "description": "Bahan katun combed 200 GSM",
        "shopee_url": "https://s.shopee.co.id/8plAFEeqEI"
    }
    cap = gen_caption(test_prod)
    print("\nCaption Preview:")
    print(cap)
