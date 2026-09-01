# ZIYAN Knowledge — AI Sales Agent & Negosiasi

Dokumen pengetahuan khusus ZIYAN tentang AI agent yang punya skill jualan/negosiasi.
Diperbarui: 2026-08-07. Referensi: riset Orion + skill 9router/cryptoskill.

## JAWABAN INTI
**Pertanyaan:** Ada kah agent yang punya skill jualan seperti Grant Cardone (video @skillforcuan)?
**Jawab:** Ada, tapi BUKAN manusia. AI sales agent sudah nyata (11x Alice, Artisan, dll).
Bedanya: Cardone = manusia ajarin anak cold call via telepon. AI agent = bot outreach digital (email/DM) otomatis.

---

## 1. FRAMEWORK AGENT (untuk bikin sales agent sendiri)

### LangChain / LangGraph
- Framework agent paling populer. Bisa bikin agent dengan tools: search, send_email, scrape.
- Dokumentasi: https://www.langchain.com/
- Pakai untuk: RISA (riset prospek), NOVA (draft outreach)

### CrewAI
- Multi-agent framework. Bisa bikin "Sales Team" (Researcher + Closer + Follow-up).
- Web: https://www.crewai.com/
- Cocok buat ZIYAN: tim agent jualan otomatis

### AutoGen (Microsoft)
- Multi-agent conversation. Bisa simulasi negosiasi antar agent.
- Pakai untuk: latih agent negosiasi (roleplay)

### GOAT (Great Onchain Agent Toolkit)
- 200+ integrasi crypto. Agent bisa wallet, swap, bridge, transaksi.
- Skill: https://cryptoskills.dev/skills/goat
- Source: https://github.com/goat-sdk/goat
- Pakai untuk: jualan produk crypto/onchain

### Coinbase AgentKit
- Framework bikin agent dengan onchain capabilities (transfer, swap, NFT).
- Skill: https://cryptoskills.dev/skills/coinbase-agentkit

---

## 2. CONTOH AGENT SALES NYATA (live product)

### 11x Alice — AI SDR (Sales Development Rep)
- Web: https://www.11x.ai/alice
- Fungsi: outbound otomatis (email/DM), turn market signals → SQL (Sales Qualified Lead)
- $70M funded (a16z, Benchmark)
- Ini yang paling mirip "agent jualan otonom"

### Artisan.ai (domain for sale — mati 2026)
- Dulu: AI sales agent "Ava" (SDR). Sekarang tutup.

### Brian API (natural language → transaksi)
- Skill: https://cryptoskills.dev/skills/brian-api
- "Swap 10 USDC for ETH" → calldata siap sign
- Pakai untuk: agent beli/jual otomatis

### x402 (HTTP 402 payment protocol)
- Skill: https://cryptoskills.dev/skills/x402
- Agent bayar microtransaction langsung lewat HTTP (stablecoin)
- Tiga aktor: Client (buyer), Resource Server (seller), Facilitator
- Pakai untuk: agent jualan digital product (template ZIYAN)

---

## 3. SKILL NEGOSIASI & PERSUASION (untuk LLM)

Tidak ada "skill negosiasi" siap pakai di repo yang Bos punya. Tapi bisa dibuat:
- **Prompt engineering**: "You are a senior sales closer. Use SPIN selling / Challenger method."
- **Roleplay dengan AutoGen**: 2 agent (buyer vs seller) latih persuasi
- **RAG**: ingest buku Cardone/Kennedy ke knowledge base → agent belajar gaya jualan

**Referensi ilmu jualan (human):**
- Grant Cardone — "The 10X Rule", cold calling
- SPIN Selling (Neil Rackham)
- Challenger Sale (Dixon/Adamson)
- Sandler Method

---

## 4. ETIKA & BATASAN (PENTING)

### Legal (Indonesia)
- UU ITE: spam/DM massal tanpa izin = ancaman pidana
- Pelanggaran ToS platform (IG/TikTok/LinkedIn) → akun banned
- Jangan impersonate manusia (deepfake voice tanpa izin)

### Best Practice ZIYAN (etis)
- Outbound: BATASI 50-100 email/hari per akun
- Selalu ada unsubscribe/opt-out
- Inbound lebih aman: bikin konten edukasi → customer datang sendiri
- Agent hanya bantu DRAFT & REPLY, bukan spam blast

### Prinsip Bos
- "Jangan jual yang bikin klien rugi" → agent jualan harus jujur
- Tidak ada hacking/bobol (sudah dilarang)

---

## 5. IMPLEMENTASI ZIYAN

### Yang sudah ada
- `cold_email_generator.json` (Sheets → Gemini → Gmail) — workflow outreach
- `ziyan-cold-email-automation` skill — panduan
- 9router proxy — model gratis untuk agent

### Yang bisa dibuat
1. **Agent Closer (CrewAI/LangGraph)**: tim riset + draft + follow-up
2. **Negosiasi RAG**: ingest buku sales → agent belajar gaya Cardone
3. **x402 integration**: jual template ZIYAN otomatis (agent bayar→download)
4. **Voice agent**: pakai TTS + STT → agent telepon kayak video Grant Cardone (tapi AI)

### Roadmap
- Fase 1: cold email (sudah ada) → tes ke 10 lead
- Fase 2: bikin CrewAI sales team
- Fase 3: negosiasi RAG + voice agent

---

## 6. SUMBER VALID (10 URL)
1. 11x Alice: https://www.11x.ai/alice
2. LangChain: https://www.langchain.com/
3. CrewAI: https://www.crewai.com/
4. GOAT: https://cryptoskills.dev/skills/goat
5. Coinbase AgentKit: https://cryptoskills.dev/skills/coinbase-agentkit
6. Brian API: https://cryptoskills.dev/skills/brian-api
7. x402: https://cryptoskills.dev/skills/x402
8. GOAT GitHub: https://github.com/goat-sdk/goat
9. 11x About: https://www.11x.ai/about-us
10. AgentSkills format: https://agentskills.io/home

## CATATAN
- RISA (sub-agent) GAGAL cari web mandiri (hanya buat todo). Orion ambil alih riset ini.
- Video @skillforcuan = manusia (Grant Cardone), BUKAN AI agent.
- AI sales agent nyata = 11x Alice (outbound otomatis).
