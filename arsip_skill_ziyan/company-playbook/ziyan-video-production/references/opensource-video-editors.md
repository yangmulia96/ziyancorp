# Open-Source Video Editors (alternatif NotebookLM / pengganti OpenMontage)

Bos minta bedah "CapCut open-source" (2026-08-02). Hasil riset GitHub:

## Kandidat (stars per 2026-08-02)
| Repo | Stars | Catatan |
|---|---|---|
| `OpenCut-app/OpenCut` | 80K | "open-source CapCut alternative" — paling populer, fokus edit video browser-based |
| `Augani/openreel-video` | 4.6K | browser-based pro editor |
| `pireel/pireel` | 868 | alternatif CapCut/ChatCut, "drivable by any AI agent" |
| `msgbyte/cutia` | 827 | in-browser CapCut alt |
| `0xsline/OpenChatCut` | 743 | local-first conversational AI video editor |
| `ter-9001/WannaCut` | 272 | CapCut alt Linux/Windows |
| `Hommy-master/capcut-mate` | 1.5K | automation toolkit untuk CapCut (API/plugin) |

## Yang perlu dibedah sebelum pakai (belum diuji)
- Apakah punya **CLI / headless mode** yang bisa agent panggil (bukan cuma UI web)?
- Apakah ada **REST API** untuk auto-edit (import assets → render → export)?
- Butuh API key berbayar (seperti CapCut Pro) atau 100% lokal gratis?
- Format export: MP4 1080x1920 (Shorts) tersedia?

## Status
- OpenMontage SUDAH DIHAPUS (pelajaran pahit: 27 mnt/video, API mati, cuma image stills).
- NotebookLM tetap jalur utama (via computer_use, Bos login sekali).
- OpenCut = calon cadangan kalau butuh edit video lokal yang bisa diotomatisasi.
- JANGAN langsung clone & generate tanpa bedah API dulu (hindari buang waktu seperti OpenMontage).
