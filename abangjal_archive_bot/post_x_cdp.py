import subprocess
import time
import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

# 1. Matikan proses chrome lama
subprocess.run(['powershell', '-Command', 'Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue'], capture_output=True)
time.sleep(2)

# 2. Buka Chrome dengan Remote Debugging Port 9222
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data = r"C:\Users\arija\AppData\Local\Google\Chrome\User Data"

proc = subprocess.Popen([
    chrome_exe,
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data}",
    "--profile-directory=Profile 2",
    "--headless=new",
    "--disable-gpu"
])
time.sleep(5)

async def test_x():
    async with async_playwright() as p:
        print("1. Menghubungkan ke Chrome via CDP (127.0.0.1:9222)...")
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        
        print("2. Membuka https://x.com/compose/post ...")
        await page.goto("https://x.com/compose/post", wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(4)
        print("   URL saat ini:", page.url)
        
        # Ketik Tweet
        tweet_text = "Uji Coba Sistem Distribusi Otomatis Arijal Meutuwah di X 🚀 #ArijalMeutuwah #OutfitPria #ShopeeAffiliate"
        
        # Selector kotak tweet
        box = page.locator('div[role="textbox"]').first
        if await box.is_visible(timeout=8000):
            print("3. Kotak input ditemukan! Mengetikkan naskah...")
            await box.click()
            await box.fill(tweet_text)
            await asyncio.sleep(2)
            
            # Selector tombol post
            btn = page.locator('button[data-testid="tweetButton"]').first
            if await btn.is_visible(timeout=5000):
                print("4. Mengklik tombol Post...")
                await btn.click()
                await asyncio.sleep(5)
                print("\n✅ TWEET BERHASIL DI-POSTING KE X (@Abangjal)!")
            else:
                print("❌ Tombol post tidak muncul.")
        else:
            print("❌ Kotak input X tidak ditemukan atau butuh login.")
            
        await browser.close()

try:
    asyncio.run(test_x())
finally:
    proc.terminate()
