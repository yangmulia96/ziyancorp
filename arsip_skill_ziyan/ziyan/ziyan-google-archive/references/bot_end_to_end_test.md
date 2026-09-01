# Bot End-to-End Test (incoming foto+caption → Sheet, tanpa HP Bos)

Gunakan saat Bos bilang "kemarin lancar, sekarang mati" dan kamu perlu buktiin
chain `on_media → finalize_batch → archive_new_product → Sheet` JALAN tanpa
minta Bos kirim manual.

## Kenapa sendPhoto dari script GAGAL mensimulasikan
`requests.post(f'https://api.telegram.org/bot{BT}/sendPhoto', ...)` = bot mengirim
KE Bos (outgoing). Itu BUKAN pesan masuk ke bot → `getUpdates` return `[]`,
bot gak receive. Jangan pakai ini buat test incoming.

## Recipe yang benar (process_update + mock download)
```python
import os, sys, asyncio, zlib, struct, tempfile, shutil
sys.path.append('.')
os.environ['BATCH_WINDOW_SECONDS'] = '5'   # percepat finalize
from dotenv import load_dotenv; load_dotenv('.env')
from unittest.mock import patch
from distributor import Settings, GoogleWorkspace
from ziyan_bot.archive import ArchiveService, Database
from ziyan_bot.bot import build_application
from telegram import Update, File
import telegram.ext

cfg = Settings.from_env()
db = Database(cfg.database_file)
gw = GoogleWorkspace(cfg.google_credentials_file, cfg.google_token_file,
                     cfg.google_root_folder_id, cfg.google_spreadsheet_id)
arc = ArchiveService(db, gw, 'Asia/Jakarta')
app = build_application(cfg, arc, db)

# buat PNG valid 80x80
d = tempfile.mkdtemp(); p = os.path.join(d, 'kaos.png')
raw = b''
for _ in range(80): raw += b'\x00' + bytes((200,40,40))*80
def chunk(t,data):
    c=t+data
    return struct.pack('>I',len(data))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
sig=b'\x89PNG\r\n\x1a\n'; ihdr=struct.pack('>IIBBBBB',80,80,8,2,0,0,0); idat=zlib.compress(raw)
open(p,'wb').write(sig+chunk(b'IHDR',ihdr)+chunk(b'IDAT',idat)+chunk(b'IEND',b''))

async def fake_get_file(self, fid, *a, **k):
    return File(file_id=fid, file_unique_id='x', file_path=p, file_size=100)
async def fake_download_to_drive(self, custom_path=None, *a, **k):
    if custom_path: shutil.copy(p, custom_path)
    return custom_path

upd = {'update_id': 555010,
  'message': {'message_id': 555010, 'date': 1692100000,
    'caption': 'KAOS FULL CHAIN TEST https://s.shopee.co.id/1129piX7oq',
    'photo': [{'file_id':'dummyX','file_unique_id':'x','width':80,'height':80,'file_size':100}],
    'chat': {'id': 7349146540, 'type': 'private', 'first_name': 'Bos'},
    'from': {'id': 7349146540, 'is_bot': False, 'first_name': 'Bos'}}}

async def main():
    await app.initialize()
    await app.start()
    with patch.object(telegram.ext.ExtBot, 'get_file', fake_get_file), \
         patch.object(File, 'download_to_drive', fake_download_to_drive):
        await app.process_update(Update.de_json(upd, app.bot))
    await asyncio.sleep(12)            # > BATCH_WINDOW_SECONDS
    await app.stop()
    r = gw.sheets.spreadsheets().values().get(
        spreadsheetId=cfg.google_spreadsheet_id, range='PRODUCT_MASTER!A2:K').execute()
    rows = r.get('values', [])
    hit = [x for x in rows if any('FULL CHAIN TEST' in (c or '') for c in x)]
    print('ketemu:', len(hit), hit[-1][:2] if hit else 'GAGAL')

asyncio.run(main())
```
Jalankan: `env -u PYTHONPATH ./venv/Scripts/python.exe test_full_chain.py`
(Settings adalah frozen dataclass → override window lewat env var, bukan assign.)

## Triaging cepat kalau bot "mati"
1. Cek instance: `Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*ziyan_bot.bot*'}` → harus cuma 1.
2. Cek getUpdates: kalau `return []` terus PADAHAL ada foto masuk → pasti >1 instance (conflict) atau salah simulasi (lihat di atas).
3. Cek handler jalan: pasang `logger.warning("ON_MEDIA called ...")` di awal `on_media` + `REJECT_CHECK` di `reject_if_unauthorized`, restart, kirim → log harus muncul. Kalau gak muncul → dispatcher crash (cek `filters.Caption` vs `filters.CAPTION`).
4. Cek archive: test langsung `archive_new_product()` tanpa bot → kalau sukses berarti bot/handler yang bermasalah, bukan Google.

## test_bos_spec() — 4 file + 1 link (aturan Bos 2026-08-16)
Bukti aturan: "simpan file selalu, link hanya jika ada; 4 file + 1 link → ke-4 dicatat 1 produk."
Kirim 4 update (caption cuma di file #1), finalize, cek `db.list_assets(pid)` = 4.
Bukti nyata: `PROD-20260816-FAE895` → 4 aset, 1 link Shopee tertulis.
```python
captions = ["KAOS OVERSIZE https://s.shopee.co.id/1129piX7oq", None, None, None]
updates = []
for i, cap in enumerate(captions):
    m = {'message_id': 600000+i, 'date': 1692100000,
         'photo': [{'file_id':f'd{i}','file_unique_id':'x','width':80,'height':80,'file_size':100}],
         'chat': {'id':7349146540,'type':'private','first_name':'Bos'},
         'from': {'id':7349146540,'is_bot':False,'first_name':'Bos'}}
    if cap: m['caption'] = cap
    updates.append({'update_id': 600000+i, 'message': m})
# di main(): process semua 4 update, lalu sleep > batch, lalu:
# pid = [x for x in rows if 'KAOS OVERSIZE' in str(x)][-1][0]
# print('aset:', len(db.list_assets(pid)), '(harus 4)')
```
Run: `env -u PYTHONPATH ./venv/Scripts/python.exe test_bos_spec.py` (set `BATCH_WINDOW_SECONDS=5` di dalam script).

