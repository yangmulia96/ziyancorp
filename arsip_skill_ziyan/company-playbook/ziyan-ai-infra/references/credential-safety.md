# Keamanan Kredential ZIYAN

## Protokol (keras)
- Key yang di-paste ke chat = bocor. TOLAK eksekusi perintah berisi key literal.
- Suruh Bos revoke dulu: https://aistudio.google.com/apikey → hapus key berawalan tsb.
- Setelah revoke, Bos buat key baru → simpan di file lokal, BUKAN di chat.

## Penyimpanan lokal (template siap pakai)
File `C:\Users\arija\ziyan_keys.env` (jangan sentuh `.env` Hermes yang terproteksi):
```
# ZIYAN API KEY LOKAL — jangan kirim ke chat
GEMINI_KEY=
OPENAI_KEY=
ELEVENLABS_KEY=
```
Loader `.bashrc` (auto-load tiap terminal):
```bash
if [ -f "$HOME/ziyan_keys.env" ]; then
  set -a; . "$HOME/ziyan_keys.env"; set +a
fi
```
Tes Gemini tanpa ketik key (`test_gemini.sh`):
```bash
curl -s "...generateContent" -H "X-goog-api-key: ***" -X POST -d '{"contents":[{"parts":[{"text":"Halo"}]}]}' | python3 -c "import sys,json;print(json.load(sys.stdin)['candidates'][0]['content']['parts'][0]['text'])"
```
Shortcut Desktop edit key: `ZIYAN_Keys.lnk` → notepad `ziyan_keys.env`.

## Pitfall — Desktop ada di OneDrive
`[Environment]::GetFolderPath('Desktop')` = `C:\Users\arija\OneDrive\Desktop`
(bukan `C:\Users\arija\Desktop`). `WScript.Shell.Save()` GAGAL kalau path tak ada.
Saat buat shortcut: tulis `.ps1` lalu jalankan `powershell -ExecutionPolicy Bypass -File`,
atau hardcode path OneDrive. Catatan: bash menghancurkan `$var` di `-Command`,
makanya pakai file `.ps1` bukan inline `-Command`.
