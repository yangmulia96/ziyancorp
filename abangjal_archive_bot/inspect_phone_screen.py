import asyncio, sys, os
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel="chrome")
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        await page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded")
        await asyncio.sleep(4)
        
        await page.locator('input[name="username_or_email"]').first.fill("abangjal")
        await page.locator('button:has-text("Continue")').first.click()
        await asyncio.sleep(4)
        
        await page.locator('input[name="password"]').first.fill("arijal1996")
        await page.locator('button:has-text("Log in"), div[role="button"]:has-text("Log in")').first.click()
        await asyncio.sleep(6)
        
        print("URL aktif:", page.url)
        # Ambil screenshot
        screen_path = r"C:\Users\arija\ziyancorp\phone_screen_detail.png"
        await page.screenshot(path=screen_path)
        print(f"Screenshot disimpan ke: {screen_path}")
        
        text = await page.locator("body").inner_text()
        print("\n=== SEMUA TEKS DI LAYAR ===")
        print(text)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
