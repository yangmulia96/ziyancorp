#!/usr/bin/env python3
"""
ZIYAN Content Distribution Pipeline - Scheduler & Persona Generator
Persona: AI Influencer "Arijal Meutuwah"
Target: YouTube (Shorts), Instagram, Facebook, Threads, Twitter / X

4 Slot Waktu Harian (WIB):
- Slot 1: 08:37 WIB
- Slot 2: 11:03 WIB
- Slot 3: 15:34 WIB
- Slot 4: 19:03 WIB
"""

from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from typing import List, Dict, Any

SLOT_TIMES = [
    time(8, 37),   # Slot 1: 08:37 WIB
    time(11, 3),   # Slot 2: 11:03 WIB
    time(15, 34),  # Slot 3: 15:34 WIB
    time(19, 3),   # Slot 4: 19:03 WIB
]

TIMEZONE_JAKARTA = ZoneInfo("Asia/Jakarta")


def generate_arijal_caption(shopee_url: str, title: str, description: str = "", extra_hashtags: List[str] = None) -> str:
    """
    Format Baku Caption Persona Arijal Meutuwah:
    [Link Affiliate Shopee/Tautan Produk]

    [Deskripsi/Ulasan Produk yang Menarik & Persuasif]

    #HashtagRelevan #ArijalMeutuwah #ShopeeAffiliate
    """
    url = shopee_url.strip() if shopee_url else ""
    desc = description.strip() if description else f"Rekomendasi pilihan terbaik: {title}. Kualitas mantap dan siap upgrade gayamu!"
    
    default_tags = ["#ArijalMeutuwah", "#ShopeeAffiliate", "#RekomendasiProduk", "#OutfitPria", "#FashionStyle"]
    if extra_hashtags:
        for t in extra_hashtags:
            clean_t = t if t.startswith("#") else f"#{t}"
            if clean_t not in default_tags:
                default_tags.insert(0, clean_t)
    
    tags_str = " ".join(default_tags[:5])
    return f"{url}\n\n{desc}\n\n{tags_str}"


def calculate_schedule_slots(file_count: int, start_from: datetime = None) -> List[datetime]:
    """
    Menghitung jadwal upload untuk N file media ke dalam 4 slot waktu harian WIB:
    Slot 1: 08:37 WIB | Slot 2: 11:03 WIB | Slot 3: 15:34 WIB | Slot 4: 19:03 WIB.
    Jika ada sisa file (>4), otomatis lanjut ke slot hari berikutnya.
    """
    now = start_from or datetime.now(TIMEZONE_JAKARTA)
    current_date = now.date()
    
    scheduled_slots = []
    
    while len(scheduled_slots) < file_count:
        for t in SLOT_TIMES:
            slot_dt = datetime.combine(current_date, t, tzinfo=TIMEZONE_JAKARTA)
            if slot_dt > now:
                scheduled_slots.append(slot_dt)
                if len(scheduled_slots) == file_count:
                    break
        current_date += timedelta(days=1)
        now = datetime.combine(current_date, time(0, 0), tzinfo=TIMEZONE_JAKARTA)
        
    return scheduled_slots


def split_product_into_queue_items(product: Dict[str, Any], assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Memecah 1 Batch Produk menjadi antrean terpisah per File Media (1 File = 1 Post PENDING).
    """
    if not assets:
        return []
    
    slots = calculate_schedule_slots(len(assets))
    queue_items = []
    
    for i, asset in enumerate(assets):
        scheduled_at = slots[i]
        caption = generate_arijal_caption(
            shopee_url=product.get("shopee_url", ""),
            title=product.get("title", ""),
            description=product.get("description", "")
        )
        
        queue_items.append({
            "product_id": product.get("product_id"),
            "asset_id": asset.get("asset_id"),
            "original_name": asset.get("original_name"),
            "drive_file_id": asset.get("drive_file_id"),
            "drive_file_url": asset.get("drive_file_url"),
            "asset_type": asset.get("asset_type"),  # photo atau video
            "shopee_url": product.get("shopee_url"),
            "caption": caption,
            "scheduled_time": scheduled_at.isoformat(),
            "scheduled_display": scheduled_at.strftime("%d-%m-%Y %H:%M WIB"),
            "status": "PENDING"
        })
        
    return queue_items
