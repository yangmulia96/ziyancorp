# Archive Bot Debugging Recipe (verified 2026-08-16)

## Problem
Bot polls `getUpdates` 200 OK but never processes incoming photos/files. Or `finalize_batch`
silently drops the archive with a network error. Root causes found this session:
1. `filters.Caption` (class) crashes the dispatcher → no handler runs at all.
2. `finalize_batch` calls `send_chat_action` first → `httpx.ReadError` aborts the whole archive.
3. `upload_file` gets a `str` instead of `Path` → crash on `path.name`.
4. Multiple orphan bot instances → `getUpdates` Conflict 409, bot appears "offline".

## Verify handler logic WITHOUT Telegram (offline sim)
`bot{BT}/sendPhoto` is OUTGOING (bot→user), it does NOT reach the bot's own `on_media`.
Drive `process_update` instead. The ExtBot rejects setting `get_file` directly
(`AttributeError: can't set`), so patch the class:

```python
import os, sys, asyncio, zlib, struct, tempfile, shutil
sys.path.append('.')
os.environ['BATCH_WINDOW_SECONDS'] = '5'   # speed up finalize for the test
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

# make a valid tiny PNG at p
d = tempfile.mkdtemp(); p = os.path.join(d, 'kaos.png')
raw = b''.join(b'\x00' + bytes((200,40,40))*80 for _ in range(80))
def chunk(t,data):
    c=t+data
    return struct.pack('>I',len(data))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
sig=b'\x89PNG\r\n\x1a\n'; ihdr=struct.pack('>IIBBBBB',80,80,8,2,0,0,0)
open(p,'wb').write(sig+chunk(b'IHDR',ihdr)+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))

async def fake_get_file(self, fid, *a, **k):
    return File(file_id=fid, file_unique_id='x', file_path=p, file_size=100)
async def fake_download_to_drive(self, custom_path=None, *a, **k):
    if custom_path: shutil.copy(p, custom_path)
    return custom_path

upd = {'update_id': 555010, 'message': {
    'message_id': 555010, 'date': 1692100000,
    'caption': 'KAOS TEST https://s.shopee.co.id/1129piX7oq',
    'photo': [{'file_id':'d1','file_unique_id':'x','width':80,'height':80,'file_size':100}],
    'chat': {'id': 7349146540, 'type': 'private', 'first_name': 'Bos'},
    'from': {'id': 7349146540, 'is_bot': False, 'first_name': 'Bos'}}}

async def main():
    await app.initialize(); await app.start()
    with patch.object(telegram.ext.ExtBot, 'get_file', fake_get_file), \
         patch.object(File, 'download_to_drive', fake_download_to_drive):
        await app.process_update(Update.de_json(upd, app.bot))
    print('update processed; waiting for finalize job...')
    await asyncio.sleep(12)
    await app.stop()
    r = gw.sheets.spreadsheets().values().get(
        spreadsheetId=cfg.google_spreadsheet_id, range='PRODUCT_MASTER!A2:K').execute()
    rows = r.get('values', [])
    hit = [x for x in rows if any('KAOS TEST' in (c or '') for c in x)]
    print('Sheet rows:', len(rows), '| hit:', len(hit))
    print('OK' if hit else 'FAIL — archive did not land')

asyncio.run(main())
```

## Check the live bot (after a real send)
```bash
# exactly ONE process must run
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%ziyan_bot.bot%'\" | Select-Object ProcessId"
# logs
grep -E "ON_MEDIA|REJECT_CHECK|finalize|DISPATCH ERROR|Produk berhasil" bot_debug.log
```
If `getUpdates` returns `[]` forever and no `ON_MEDIA` appears, check for orphan instances
(kill all, start one) BEFORE assuming the handler is broken.

## Confirm archive reached Drive + Sheet
```python
from distributor import Settings, GoogleWorkspace
s = Settings.from_env()
gw = GoogleWorkspace(s.google_credentials_file, s.google_token_file,
                     s.google_root_folder_id, s.google_spreadsheet_id)
pm = gw.sheets.spreadsheets().values().get(
    spreadsheetId=s.google_spreadsheet_id, range='PRODUCT_MASTER!A2:B').execute()
for row in pm.get('values', []):
    print(row[0], '|', (row[1][:40] if len(row) > 1 else ''))
```
