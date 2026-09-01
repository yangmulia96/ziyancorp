import subprocess
import time
import asyncio
import os
import shutil
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

# 1. Buat folder temporary automation profile
auto_dir = r"C:\Users\arija\AppData\Local\Google\Chrome\User Data\AutomationProfile"
os.makedirs(auto_dir, exist_ok=True)

# Copy Local State
src_user_data = r"C:\Users\arija\AppData\Local\Google\Chrome\User Data"
shutil.copy2(os.path.join(src_user_data, "Local State"), os.path.join(auto_dir, "Local State"))

# Copy Profile 2 to Default in auto_dir
target_prof = os.path.join(auto_dir, "Default")
os.makedirs(os.path.join(target_prof, "Network"), exist_ok=True)

# Copy Cookies & Preferences & Storage
shutil.copy2(os.path.join(src_user_data, "Profile 2", "Preferences"), os.path.join(target_prof, "Preferences"))
if os.path.exists(os.path.join(src_user_data, "Profile 2", "Network", "Cookies")):
    shutil.copy2(os.path.join(src_user_data, "Profile 2", "Network", "Cookies"), os.path.join(target_prof, "Network", "Cookies"))

print("=== MELUNCURKAN PLAYWRIGHT DENGAN PROFIL SESI ARIJAL ===")

async def test_x():
    async with async_playwright() as p:
        print("1. Meluncurkan Chrome Browser Automation...")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=auto_dir,
            channel="chrome",
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("2. Membuka https://x.com/home ...")
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(4)
        print("   URL saat ini:", page.url)
        
        # Buka compose
        print("3. Membuka https://x.com/compose/post ...")
        await page.goto("https://x.com/compose/post", wait_until="domcontentloaded")
        await asyncio.sleep(4)
        
        tweet_text = "Uji Coba Distribusi Otomatis Arijal Meutuwah di X 🚀 #ArijalMeutuwah #OutfitPria #ShopeeAffiliate"
        
        # Cari kotak input
        box = page.locator('div[role="textbox"]').first
        if await box.is_visible(timeout=8000):
            print("4. Kotak input ditemukan! Mengetikkan tweet...")
            await box.click()
            await box.fill(tweet_text)
            await asyncio.sleep(2)
            
            btn = page.locator('button[data-testid="tweetButton"]').first
            if await btn.is_visible(timeout=5000):
                print("5. Mengklik tombol Post...")
                await btn.click()
                await asyncio.sleep(5)
                print("\n✅ TWEET BERHASIL DI-POSTING KE AKUN X (@Abangjal)!")
            else:
                print("❌ Tombol post tidak ditemukan.")
        else:
            print("❌ Kotak input X tidak ditemukan (Kemungkinan butuh login / CAPTCHA di URL:", page.url, ")")
            
        await context.close()

asyncio.run(test_x())
