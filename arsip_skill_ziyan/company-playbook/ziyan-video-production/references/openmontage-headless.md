# JALUR C — OpenMontage headless (repo `C:\Users\arija\ziyan_openmontage`)

Terverifikasi 2026-08-02: 1 Short portrait 1080x1920 / 53s, narasi TTS, dari naskah
`ziyan_content_day1/shorts_a1.txt`. Output `ziyan_videos/openmontage_shorts_a1.mp4`.

## Rule Zero (kontrak repo)
Repo punya `AGENTS.md` yang MEWAJIBKAN baca `AGENT_GUIDE.md` sebelum apa pun, dan semua
produksi HARUS lewat pipeline (`pipeline_defs/<name>.yaml`) + tool registry — bukan skrip
API ad-hoc. Baca `AGENT_GUIDE.md` + manifest pipeline dulu, selalu.

## ⚠️ PITFALL #1 (paling sering bikin gagal total): PYTHONPATH bocor
Terminal Hermes menyuntikkan venv `hermes-agent` ke `PYTHONPATH`. `registry.discover()`
langsung crash: `ModuleNotFoundError: No module named 'rpds.rpds'` (jsonschema ketarik dari
venv Hermes, bukan venv OpenMontage). FIX: prefix SETIAP perintah dengan `PYTHONPATH=`:

```bash
cd /c/Users/arija/ziyan_openmontage && PYTHONPATH= .venv/Scripts/python.exe <script.py>
```

(Pola sama seperti pitfall pyttsx3/pywintypes di `offline-pyttsx3-ffmpeg.md` — akar masalahnya identik.)

## Alur yang berhasil
1. **Preflight** — `registry.discover()` lalu `registry.provider_menu_summary()`.
   JANGAN print `support_envelope()` (megabyte JSON). Ringkas per-capability saja:
   `for c in s['capabilities']: print(c['capability'], c['configured'],'/',c['total'])`.
2. **Init workspace** — `from lib.checkpoint import init_project; init_project('<kebab-id>', title=..., pipeline_type='animated-explainer')`
   → bikin `projects/<id>/{artifacts,assets,renders}`. Semua output WAJIB di bawah sini.
3. **Assets** — narasi + gambar (lihat status provider di bawah).
4. **Artifacts** — tulis `asset_manifest.json` + `edit_decisions.json` sendiri
   (`render_runtime`, `profile`, `cuts[]` dengan `in_seconds`/`out_seconds`, `audio.narration.segments[]`
   yang menunjuk `asset_id`).
5. **Compose** — `registry._tools['hyperframes_compose'].execute({operation:'render', workspace_path, output_path,
   edit_decisions, asset_manifest, playbook, profile, quality, fps, skip_contrast:True})`.
   Tool ini scaffold HTML+GSAP → lint → validate → render MP4. Semua tool dipanggil `.execute(dict)`
   dan balikin `ToolResult(.success/.data/.error)` — bukan `.run()`.

## ⚠️ PITFALL #2: nama media profile harus valid, kalau tidak diam-diam jadi landscape
`_resolve_dimensions()` fallback ke **1920x1080** tanpa error kalau nama profile tak dikenal.
`"tiktok_vertical"` TIDAK ADA → hasil landscape walau render "sukses". Nama valid ada di
`lib/media_profiles.py`: `youtube_shorts`, `instagram_reels`, `tiktok`, `youtube_landscape`,
`youtube_4k`, `instagram_feed`, `linkedin`, `cinematic`, `generic_hd`.
Untuk Short pakai **`youtube_shorts`** (1080x1920). Selalu verifikasi `data['width']/['height']`
di hasil render DAN `ffprobe` file akhir.

## Runtime komposisi di laptop ini
- `ffmpeg` ✅, `hyperframes` ✅, `remotion` ❌ (`remotion-composer/node_modules` belum di-install).
- HyperFrames butuh Chrome headless sekali saja: `npx -y hyperframes browser ensure` (~115 MB, sekali).
  Cek dulu `npx -y hyperframes doctor`. RAM laptop 7.8 GB → doctor warning low-memory tapi render 53s tetap jalan.
- Registry `discover()` bisa lambat & keluarkan warning `hyperframes: npm package not resolvable: timeout (5s)` —
  itu cuma probe registry npm, bukan penghalang.

## Status provider dengan GEMINI key gratis (AI Studio)
| Jalur | Status | Catatan |
|---|---|---|
| `gemini-2.5-flash-preview-tts` REST | ✅ JALAN | satu-satunya TTS gratis yang tembus |
| tool `google_tts` / `tts_selector` | ❌ 401 | tool pukul **Cloud TTS API** (`texttospeech.googleapis.com`) yang butuh GCP project, bukan key AI Studio |
| `imagen-4.0-*` (`google_imagen`) | ❌ 404 | "no longer available to new users" — semua varian base/fast/ultra |
| `gemini-*-image` (nano-banana) | ❌ 429 | free tier tanpa kuota image |
| video_gen (veo/FAL/Replicate/Runway/Kling) | ❌ | butuh billing / key berbayar |

Upgrade termurah & GRATIS: `PEXELS_API_KEY` + `PIXABAY_API_KEY` → langsung buka stock image
DAN stock video di `image_selector`/`video_selector`. Tawarkan ini ke Bos sebelum minta yang berbayar.

## Resep Gemini TTS REST (fallback saat `google_tts` 401)
POST `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=...`
body: `contents[].parts[].text` (prefix instruksi delivery, mis. "Say in an energetic, punchy YouTube Shorts narrator voice: ..."),
`generationConfig.responseModalities=["AUDIO"]`, `speechConfig.voiceConfig.prebuiltVoiceConfig.voiceName="Charon"`.
Balikan = **PCM mentah base64 (24 kHz, mono, 16-bit)** di `candidates[0].content.parts[0].inlineData.data`
→ WAJIB dibungkus header WAV sendiri, kalau tidak file tak terbaca:

```python
def wav(pcm, rate=24000):
    import struct
    return (b"RIFF" + struct.pack("<I", 36+len(pcm)) + b"WAVEfmt "
            + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate*2, 2, 16)
            + b"data" + struct.pack("<I", len(pcm)) + pcm)
```
Sleep ~3s antar segmen + retry pada 429.

## Timing tanpa image
Durasi tiap cut = `ffprobe` durasi WAV narasi + gap ~0.55s. Total 7 segmen naskah A1 = 53.4s (target ~60s, OK).

## Kejujuran pelaporan (wajib)
Tanpa image gen, hasil = **kinetic text-card** (bukan visual AI). Itu DEVIASI dari pipeline
image-led dan pemakaian TTS langsung adalah deviasi dari `tts_selector`. Laporkan kedua deviasi
eksplisit ke Bos beserta tabel gagal/berhasil — jangan diam-diam substitusi
(AGENT_GUIDE "No Unilateral Substitutions").

## Verifikasi akhir
`ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height -of default=nw=1 <mp4>`
→ harus 1080x1920, ada stream audio aac. Cek juga 1 frame (`ffmpeg -ss N -frames:v 1`) dan
histogram warna via Pillow untuk memastikan bukan layar hitam kosong.
**Path Windows:** `ffprobe` di sini gagal baca path gaya MSYS `/c/Users/...` → pakai `C:\Users\...`.
