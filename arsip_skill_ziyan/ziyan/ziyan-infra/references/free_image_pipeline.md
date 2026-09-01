# ZIYAN - Pipeline Generate Gambar GRATIS (terverifikasi 2026-08-07)

## Kesimpulan cepat
- **Higgsfield CLI** = berbayar (credit). CLI jalan, tapi `auth login` gagal server-side (OAuth scope `user:org:read` ditolak Clerk). Tidak bisa dipakai untuk free gen sekarang.
- **Nano Banana / Gemini Flash Image** = "gratis" di teori (free tier AI Studio), TAPI `GEMINI_KEY` Bos quota=0 dan 9router channel `gemini/*-image` -> 429. Tidak usable sekarang.
- **FLUX via Cloudflare di 9router** = GRATIS & JALAN 100%. Ini jalur gratis yang pasti hidup.

## Model image 9router yang JALAN (test 2026-08-07)
- `cf/@cf/black-forest-labs/flux-2-dev` -> 200, return JPEG base64 (~248KB). PAKAI INI default.
- `cf/@cf/black-forest-labs/flux-2-klein-4b` (ringan)
- `cf/@cf/black-forest-labs/flux-1-schnell` (cepat)
- `cf/@cf/leonardo/phoenix-1.0`, `cf/@cf/leonardo/lucid-origin`
- `cf/@cf/stabilityai/stable-diffusion-xl-base-1.0`
- `ag/gemini-3.1-flash-image` (setara Nano Banana 2, gratis lewat proxy Antigravity - cek skill utama)

## Model image 9router yang MATI
- `gemini/gemini-2.5-flash-image` -> 429 (quota free tier=0)
- `gemini/gemini-3.1-flash-image-preview` -> 429 / 400 (key proxy invalid)

## Script reusable (sudah dibuat & terbukti)
`C:\Users\arija\ziyan_tools\genimg_free.py`
```bash
python ziyan_tools/genimg_free.py "prompt" --model cf/@cf/black-forest-labs/flux-2-dev --out hasil.jpg --size 1024x1024
```
Header wajib: `Authorization: Bearer $HERMES_CUSTOM_9ROUTER_API_KEY`.
Endpoint: `POST http://127.0.0.1:20128/v1/images/generations`.
Format return: `data[0].b64_json` (JPEG/WebP/PNG - deteksi magic byte).

## Higgsfield CLI install fix (Windows)
Postinstall `npm i -g @higgsfield/cli` gagal: `install.js` lewat path backslash corrupt ke `tar` -> "Cannot connect to higgsfield\cli\vendor\...".
Fix:
```bash
npm i -g @higgsfield/cli --ignore-scripts
CLI_DIR="$APPDATA/npm/node_modules/@higgsfield/cli"
mkdir -p "$CLI_DIR/vendor"
curl -sSL -o "$CLI_DIR/vendor/hf_1.1.20_windows_amd64.tar.gz" \
  https://github.com/higgsfield-ai/cli/releases/download/v1.1.20/hf_1.1.20_windows_amd64.tar.gz
tar -xzf "$CLI_DIR/vendor/hf_1.1.20_windows_amd64.tar.gz" -C "$CLI_DIR/vendor"
higgsfield --version   # -> 1.1.20
```
Skills companion: `npx skills add higgsfield-ai/skills --yes` (LOKAL, tanpa `--global` - PromptScript tolak global install). Tersimpan di `~/.agents/skills/higgsfield-*`.
Auth: `higgsfield auth login` buka browser; tapi per 2026-08-07 gagal: "The requested scope is invalid ... 'user:org:read'". Tunggu fix server Higgsfield.
