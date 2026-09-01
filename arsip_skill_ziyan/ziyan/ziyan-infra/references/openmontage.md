# OpenMontage — Referensi Arsitektur Video Agentic (ZIYAN)

Sumber: `calesthio/OpenMontage` (44.adjusting⭐, AGPLv3). Dipelajari 2026-08-01.

## Apa itu
Sistem produksi video agentic open-source. Agent menjalankan alur: web research → naskah → cari footage/asset → narasi (TTS) → subtitle → render. Berjalan di Claude Code / Cursor / Codex / Windsurf.

## 12 pipeline utama
Documentary Montage, Explainer, Talking Head, Screen Demo, Cinematic Trailer, Animation, Podcast, Localization, dll. Tiap pipeline punya "director skill" (markdown) yang mengajar agent cara eksekusi tiap stage.

## Mode biaya
| Mode | Tool | Biaya |
|---|---|---|
| Narasi | Piper TTS (offline) | $0 |
| Footage | Archive.org, NASA, Wikimedia, Pexels, Unsplash | $0 (dev key gratis) |
| Render | Remotion (React) / HyperFrames | $0 (open-source) |
| Gambar AI | FLUX / GPT-Image | berbayar (kecuali lokal) |
| Video AI | Veo / Kling / Runway (fal.ai) | berbayar ($0.15–$1.50) |

Contoh hasil nyata (biaya): LIBRARY AT ALEXANDRIA $0.02, AFTERNOON IN CANDYLAND $0.15, VOID $0.69, THE LAST BANANA $1.33.

## Fitur kunci (bisa diadopsi ZIYAN)
- **Storyboard approval gate**: aset generate pause per-scene, klien approve SEBELUM render. Cocok prinsip etik ZIYAN ("jangan klien rugi, tunjukkan bukti dulu").
- **Web research first-class**: 15–25 search sebelum naskah → video grounded di fakta, bukan halu.
- **Budget governance**: cost estimate sebelum eksekusi, spend cap, per-action approval.
- **Quality gates**: ffprobe + frame sampling + audio analysis pasca-render.
- **No vendor lock-in**: provider selector scoring 7 dimensi.

## Kendala di laptop Bos
- Butuh Node.js + npm + Python venv (belum ada Node).
- Setup berat (700+ skill file). Mode gratis tidak butuh GPU (Piper + ffmpeg ringan).
- AGPLv3: kalau dimodifikasi & dikomersialkan (Jalur 1), wajib open-source kan kode → batasan hukum buat produk komersial.

## Sinergi ZIYAN (rekomendasi)
- NotebookLM tetap Jalur A utama. OpenMontage = referensi/pelengkap, BUKAN pengganti.
- Padanan gratis ZIYAN sudah ada: 9router Flux (image) + edge-tts (narasi) + ffmpeg (render) + computer_use.
- Lebih strategis: TIRU polanya (research→naskah→footage gratis→TTS→render + approval gate), jangan pindah total ke OpenMontage.

## URL cek hasil (buka di HP)
- Channel: https://www.youtube.com/@OpenMontage
- README embed contoh: SIGNAL FROM TOMORROW, THE LAST BANANA, LIBRARY AT ALEXANDRIA, VOID, AFTERNOON IN CANDYLAND, MORI NO SEISHIN (lihat README repo untuk asset URL).
