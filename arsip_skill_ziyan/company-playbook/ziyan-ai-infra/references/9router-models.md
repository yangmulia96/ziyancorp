# 9router — Hasil Tes Model (2026-07-31)

Proxy `http://127.0.0.1:20128/v1`, key env `HERMES_CUSTOM_9ROUTER_API_KEY`.
Header wajib: `Authorization: Bearer $KEY`.

## Model FREE — LANGSUNG JALAN (urutan prioritas rotasi)
| Prioritas | Model ID | Channel | Catatan |
|---|---|---|---|
| 1 | `google/gemma-4-31b-it:free` | Google AI Studio | Respons Indo paling bersih, to-the-point |
| 2 | `google/gemma-4-26b-a4b-it:free` | Darkbloom | Bersih, lebih ringan/cepat |
| 3 | `poolside/laguna-s-2.1:free` | Poolside | Cepat, jawaban singkat rapi |
| 4 | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Nvidia | Stabil, output bersih "Halo" |
| 5 | `nvidia/nemotron-3-super-120b-a12b:free` | Nvidia | Kapasitas besar, tugas agak berat |
| 6 | `nvidia/nemotron-3-nano-30b-a3b:free` | Nvidia | Jalan, tapi reasoning bocor ke teks |

## Cadangan (bukan :free, tetap hidup)
- `groq/llama-3.3-70b-versatile` — balas "Halo!" lancar.

## Free tapi butuh max_tokens ≥ 300 (reasoning, kurang pas tugas ringan)
- `inclusionai/ling-3.0-flash:free` — finish=length, konten kosong dgn token kecil.
- `cohere/north-mini-code:free` — sama, fokus coding.

## HINDARI (gagal/limit)
| Model ID | Error |
|---|---|
| `kr/*` (kr/auto, kr/claude-opus-5, dll) | 402 MONTHLY_REQUEST_COUNT — kuota bulanan habis |
| `kimi/*` (kimi/kimi-latest) | 402 "unable to verify membership" |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Timeout >50s (model 550B terlalu berat) |
| `poolside/laguna-xs-2.1:free` | 429 Provider rate limit |
| `poolside/laguna-m.1:free` | 429 rate limit |
| `gemini/gemini-3.6-flash` | 400 Bad request (butuh param beda) |
| `gemma-4-31b-it` (tanpa :free, paid) | "No active credentials" — butuh API key Google AI Studio |

## Script rotasi (rotasi.sh) — konsep
Loop model prioritas, test call `max_tokens=30` prompt "Halo":
- gagal (402/429/timeout/empty) → lanjut model berikutnya
- berhasil → cetak `MODEL_OK: <id>` lalu exit
File detail: `C:\Users\arija\SOP_Rotasi_Model_9router.md`, `C:\Users\arija\models9r.json`.
