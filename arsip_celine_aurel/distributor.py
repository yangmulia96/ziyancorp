#!/usr/bin/env python3
"""
Celine Aurel Distributor - Orchestrator Distribusi Multi-Platform
Persona: AI Influencer "Celine Aurel" (Wanita / Fashion / Lifestyle / Shopee Affiliate)
Target Akun: Khusus Ekosistem Celine Aurel (YouTube Shorts, IG @celineaurel99, FB Page Celine Aurel).
"""
import os, json, sys, re
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from dotenv import load_dotenv
import requests

ROOT = Path(r"C:\Users\arija\ziyancorp\arsip_celine_aurel")
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT))

from ziyan_bot.google_workspace import GoogleWorkspace
from ziyan_bot.config import Settings

NINE_ROUTER = "http://127.0.0.1:20128/v1/chat/completions"


def gen_caption(product: dict, persona: str = "Celine Aurel") -> str:
    """Caption terstruktur untuk AI Influencer 'Celine Aurel' (Shopee Affiliate).
    Format Baku:
    [Link Affiliate Shopee/Tautan Produk]

    [Deskripsi/Ulasan Produk yang Cantik & Menarik]

    #HashtagRelevan #CelineAurel #ShopeeAffiliate
    """
    url = (product.get('shopee_url') or product.get('tiktok_url') or '').strip()
    title = product.get('title') or ''
    orig_desc = product.get('description') or ''
    
    # Bersihkan teks harga & format kotor
    clean_title = re.sub(r"dengan harga Rp[0-9.]+", "", title, flags=re.I).strip()
    clean_title = re.sub(r"\. Dapatkan di Shopee sekarang!.*", "", clean_title, flags=re.I).strip()
    clean_title = re.sub(r"^Cek\s+", "", clean_title, flags=re.I).strip()

    prompt = f"""Buat caption produk untuk akun AI influencer Wanita "{persona}".
FORMAT WAJIB PERSIS (pisahkan tiap bagian dengan 1 baris kosong):
{url}

[1-2 kalimat deskripsi/ulasan produk yang manis, natural & menarik gaya {persona}, jelaskan kecocokan outfit atau look]

#CelineAurel #ShopeeAffiliate #OOTDWanita #FashionAesthetic #RekomendasiOutfit

ATURAN KETAT:
- Baris pertama HARUS link produk: {url}
- JANGAN menyebut nominal harga, diskon, atau angka rupiah.
- DILARANG menjawab seperti customer service (contoh: jangan tulis 'Saya tidak bisa mengakses...').
- Tulis langsung ulasan produknya.

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
                if content and "tidak bisa mengakses" not in content:
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
                if content and "tidak bisa mengakses" not in content:
                    return content
        except Exception:
            pass

    # 3. Fallback Template Baku Celine Aurel ($0 / Offline)
    desc_text = orig_desc if orig_desc and "http" not in orig_desc else f"Outfit cantik rekomendasi Celine hari ini: {clean_title}. Bahannya nyaman banget, potongannya pas, dan bikin look harian kamu makin aesthetic!"
    return f"{url}\n\n{desc_text}\n\n#CelineAurel #ShopeeAffiliate #OOTDWanita #FashionAesthetic"


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


def post_facebook(caption: str, page_id: str, page_token: str, media_url: str = None) -> dict:
    if not page_id or not page_token:
        return {"status": "skipped", "reason": "no_fb_token"}
    try:
        if media_url:
            is_video = True  # For now, everything we post is a video in this script
            if is_video:
                url = f"https://graph.facebook.com/v21.0/{page_id}/videos"
                data = {"description": caption, "file_url": media_url, "access_token": page_token}
            else:
                url = f"https://graph.facebook.com/v21.0/{page_id}/photos"
                data = {"caption": caption, "url": media_url, "access_token": page_token}
        else:
            url = f"https://graph.facebook.com/v21.0/{page_id}/feed"
            data = {"message": caption, "access_token": page_token}
        r = requests.post(url, data=data, timeout=30).json()
        return {"status": "success" if "id" in r else "error", "response": r}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def post_instagram(caption: str, media_url: str, ig_user_id: str, token: str) -> dict:
    if not ig_user_id or not token or not media_url:
        return {"status": "skipped", "reason": "missing_ig_params"}
    try:
        is_video = True  # For now, everything we post is a video in this script
        url_create = f"https://graph.facebook.com/v21.0/{ig_user_id}/media"
        
        payload = {
            "caption": caption[:2200],
            "access_token": token
        }
        
        if is_video:
            payload["media_type"] = "REELS"
            payload["video_url"] = media_url
        else:
            payload["image_url"] = media_url
            
        r1 = requests.post(url_create, data=payload, timeout=30).json()
        if "id" not in r1:
            return {"status": "error", "step": "create_container", "response": r1}
        
        container_id = r1["id"]
        
        # If it's a video, Instagram processes it asynchronously. We should ideally poll the status.
        # For simplicity, we just trigger publish (might fail if not ready, but we try).
        import time
        if is_video:
            print("[INFO] Menunggu Instagram memproses video (10 detik)...")
            time.sleep(10)
            
        url_pub = f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish"
        r2 = requests.post(url_pub, data={
            "creation_id": container_id,
            "access_token": token
        }, timeout=30).json()
        return {"status": "success" if "id" in r2 else "error", "response": r2}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def post_threads(text: str, media_url: str = None, token: str = None) -> dict:
    token = token or os.environ.get("THREADS_USER_TOKEN", "")
    if not token:
        return {"status": "skipped", "reason": "no_threads_token"}
    try:
        url_create = "https://graph.threads.net/v1.0/me/threads"
        is_video = True  # For now, all queue items are videos
        
        payload = {
            "media_type": "VIDEO" if is_video else ("IMAGE" if media_url else "TEXT"),
            "text": text[:500],
            "access_token": token
        }
        if media_url:
            if is_video:
                payload["video_url"] = media_url
            else:
                payload["image_url"] = media_url
                
        r1 = requests.post(url_create, data=payload, timeout=30).json()
        if "id" not in r1:
            return {"status": "error", "response": r1}
        
        cid = r1["id"]
        import time
        if is_video:
            print("[INFO] Menunggu Threads memproses video (10 detik)...")
            time.sleep(10)
            
        url_pub = "https://graph.threads.net/v1.0/me/threads_publish"
        r2 = requests.post(url_pub, data={"creation_id": cid, "access_token": token}, timeout=30).json()
        return {"status": "success" if "id" in r2 else "error", "response": r2}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def post_youtube_celine(title: str, description: str, video_path: str) -> dict:
    token_file = ROOT / "token_celine.json"
    if not token_file.exists() or not video_path or not os.path.exists(video_path):
        return {"status": "skipped", "reason": "token_or_video_missing"}
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
                "tags": ["CelineAurel", "ShopeeAffiliate", "Shorts", "OOTDWanita"],
                "categoryId": "26"
            },
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        }
        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
        res = yt.videos().insert(part="snippet,status", body=body, media_body=media).execute()
        vid_id = res.get("id")
        return {"status": "success", "platform": "youtube_celine", "url": f"https://youtube.com/shorts/{vid_id}"}
    except Exception as e:
        return {"status": "error", "platform": "youtube_celine", "error": str(e)}
