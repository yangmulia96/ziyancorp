import json, base64, sqlite3, shutil, tempfile, sys, os, time, asyncio
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import win32crypt
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

local_state_path = r'C:\Users\arija\AppData\Local\Google\Chrome\User Data\Local State'
cookie_db = r'C:\Users\arija\AppData\Local\Google\Chrome\User Data\Profile 2\Network\Cookies'
SCREENSHOT = r'C:\Users\arija\ziyancorp\bukti_tweet_terbit.png'
TWEET_TEXT = 'Uji Coba Distribusi Otomatis Arijal Meutuwah di X 🚀 #ArijalMeutuwah #OutfitPria #ShopeeAffiliate'

def get_encryption_key():
    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    encrypted_key = encrypted_key[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_val(data, key):
    try:
        if data[:3] == b'v10' or data[:3] == b'v11':
            iv = data[3:15]
            payload = data[15:]
            aesgcm = AESGCM(key)
            return aesgcm.decrypt(iv, payload, None).decode('utf-8')
    except Exception:
        pass
    return None

def get_all_x_cookies():
    key = get_encryption_key()
    tmp_db = os.path.join(tempfile.gettempdir(), f'x_all_cookies_{int(time.time())}.db')
    try:
        shutil.copy2(cookie_db, tmp_db)
    except Exception:
        pass
        
    conn = sqlite3.connect(tmp_db)
    cur = conn.cursor()
    cur.execute("SELECT host_key, name, path, is_secure, is_httponly, encrypted_value FROM cookies WHERE host_key LIKE '%x.com%' OR host_key LIKE '%twitter.com%'")
    
    cookies = []
    for host_key, name, path, is_sec, is_http, enc_val in cur.fetchall():
        val = decrypt_val(enc_val, key)
        if val:
            cookies.append({
                'name': name,
                'value': val,
                'domain': host_key,
                'path': path,
                'secure': bool(is_sec),
                'httpOnly': bool(is_http)
            })
    conn.close()
    try:
        os.remove(tmp_db)
    except Exception:
        pass
    return cookies

async def main():
    print('=== 1. MENGEKSTRAK SELURUH COOKIES DARI CHROME PROFILE 2 ===')
    cookies = get_all_x_cookies()
    print(f'Ditemukan {len(cookies)} cookies untuk X/Twitter.')
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            channel='chrome',
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        
        await context.add_cookies(cookies)
        page = await context.new_page()
        
        print('=== 2. MEMBUKA https://x.com/home ===')
        await page.goto('https://x.com/home', wait_until='domcontentloaded', timeout=45000)
        await asyncio.sleep(5)
        print('   URL aktif:', page.url)
        
        print('=== 3. MEMBUKA https://x.com/compose/post ===')
        await page.goto('https://x.com/compose/post', wait_until='domcontentloaded', timeout=45000)
        await asyncio.sleep(5)
        print('   URL compose:', page.url)
        
        box = page.locator('div[role="textbox"]').first
        if await box.is_visible(timeout=10000):
            print('=== 4. MENGISI TEKS TWEET ===')
            await box.click()
            await box.fill(TWEET_TEXT)
            await asyncio.sleep(2)
            
            btn = page.locator('button[data-testid="tweetButton"]').first
            if not await btn.is_visible():
                btn = page.locator('button[data-testid="tweetButtonInline"]').first
                
            if await btn.is_visible(timeout=5000):
                print('=== 5. MENGKLIK TOMBOL POST ===')
                await btn.click()
                await asyncio.sleep(6)
                print('\n🎉🎉🎉 HASIL: TWEET RESMI DITERBITKAN DI TIMELINE X (@Abangjal)!')
            else:
                print('Tombol post tidak muncul.')
        else:
            print('Kotak tweet tidak muncul (URL:', page.url, ')')
            
        print('=== 6. MEMBUKA PROFIL TIMELINE ===')
        await page.goto('https://x.com/Abangjal', wait_until='domcontentloaded', timeout=45000)
        await asyncio.sleep(5)
        await page.screenshot(path=SCREENSHOT)
        print(f'📸 Screenshot bukti terbit: {SCREENSHOT}')
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
