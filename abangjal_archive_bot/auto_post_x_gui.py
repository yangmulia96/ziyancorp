import time
import subprocess
import os
import sys
import pyautogui
import pyperclip

sys.stdout.reconfigure(encoding='utf-8')
pyautogui.FAILSAFE = False

print("=== MEMULAI OTOMASI POSTING X (@Abangjal) ===")

tweet_text = "Uji Coba Distribusi Otomatis Arijal Meutuwah di X 🚀 #ArijalMeutuwah #OutfitPria #ShopeeAffiliate"

# 1. Buka URL Compose di Chrome
print("1. Membuka https://x.com/compose/post di Google Chrome...")
subprocess.run(["cmd.exe", "/c", "start", "chrome", "https://x.com/compose/post"], shell=True)

# Tunggu 6 detik agar halaman X terbuka penuh dan fokus otomatis ke kotak teks
print("2. Menunggu halaman terbuka dan fokus otomatis (6 detik)...")
time.sleep(6)

# Pindahkan kursor ke tengah layar agar aman dari failsafe
pyautogui.moveTo(600, 400)
time.sleep(1)

# 2. Paste naskah tweet
print("3. Mengetikkan naskah tweet...")
pyperclip.copy(tweet_text)
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'v')
time.sleep(2)

# 3. Kirim tweet dengan shortcut Ctrl+Enter
print("4. Mengirimkan Tweet (Menekan Ctrl + Enter)...")
pyautogui.hotkey('ctrl', 'enter')
time.sleep(4)

# 4. Ambil screenshot layar penuh sebagai bukti
screenshot_path = r"C:\Users\arija\ziyancorp\bukti_posting_x.png"
img = pyautogui.screenshot()
img.save(screenshot_path)
print(f"5. Screenshot bukti disimpan di: {screenshot_path}")

print("\n🎉 POSTING TEST DI X TELAH BERHASIL DIKIRIMKAN!")
