# Content Factory Architecture Reference

Sumber: Analisis 4 video YouTube (channel ADANG HDYT) + implementasi ZIYAN.

---

## 4 Model Arsitektur

### Model 1: Image-to-Video Affiliate (Promosi & UGC)
- **Use Case**: Sistem 2 (AI Influencer Content Engine)
- **Alur**: Foto produk → Nano Banana (Google AI Studio edit) → Kling AI/Sora (gerak) → Telegram Bot trigger → Video review
- **Biaya**: ~Rp0-5k/video (gratis tier)
- **Tools Kunci**: Nano Banana (image edit), Kling AI/Sora (video), EA Agent (prompt engineering)
- **Status ZIYAN**: Butuh Fal.ai key + Kling AI API + Nano Banana workaround

### Model 2: Batch Sheets → Video UGC (Review Produk)
- **Use Case**: Sistem 3 (Value-First Help + Systematic Tracking)
- **Alur**: Google Sheets (batch) → Maya Router (prompt lokal) → Sora 2/Kling AI (Avatar talking head) → Google Drive → Update Sheets
- **Biaya**: ~Rp2.500/video (terukur)
- **Tools Kunci**: Google Sheets/Drive API, Maya Router, Sora 2/Kling AI
- **Status ZIYAN**: Sheets/Drive ready, butuh Kling/Sora API

### Model 3: Faceless Storytelling (Tuyul Digital)
- **Use Case**: Konten educational/storytelling (bonus)
- **Alur**: Schedule Trigger → OpenAI (ide) → Fal.ai (Flux + Kling paralel) → MMAudio (SFX) → FFmpeg (gabung 13 klip x 5s)
- **Biaya**: ~Rp43.000/video
- **Target**: TikTok Creativity Program + AdSense
- **Status ZIYAN**: Butuh Fal.ai + OpenAI + FFmpeg lokal

### Model 4: Massal Zero-Cost (RISIKO TINGGI)
- **Use Case**: Brand awareness ONLY, JANGAN untuk monetisasi
- **Alur**: DeepSeek V3 (quotes) → FFmpeg batch render lokal (background + typography + musik) → 1000 video/run
- **Risiko**: Demonetisasi Reused Content
- **Status ZIYAN**: SKIP untuk monetisasi utama

---

## Tool Stack Mapping

| Tool | Fungsi | Provider | Cost |
|------|--------|----------|------|
| **Fal.ai** | Flux (image), Kling (video), MMAudio (SFX) | Cloud API | Pay-per-use (~$0.02-0.05/video) |
| **Kling AI** | Cinematic Image-to-Video | Kuaishou API | Apply required |
| **Nano Banana** | Image editing (bg swap, pose, model) | Google AI Studio | **No official API** - workaround needed |
| **Maya Router** | Local prompt routing | Open source | Free |
| **MMAudio** | Video-to-audio SFX sync | Fal.ai/Replicate | Included in Fal.ai |
| **FFmpeg** | Local video stitch/render | Local CLI | Free |
| **ElevenLabs** | TTS Voiceover | API | ~$0.01/char |

---

## ZIYAN Implementation Priority

1. **Sistem 2 (AI Influencer)** → Model 1 pattern
   - Need: Fal.ai key, Kling API, Nano Banana workaround (Gemini/Imagen via 9Router)
   
2. **Sistem 3 (Value-First Help)** → Model 2 pattern  
   - Need: Google Sheets API ✅, Kling/Sora API, Maya Router (n8n node)
   
3. **n8n Orchestration** → Both models
   - HTTP Request nodes ke Fal.ai, Google Sheets, Drive
   - Schedule: Generate 8min, Publish 77min (anti-spam)

4. **Skip Model 4** - High risk, low reward for monetization