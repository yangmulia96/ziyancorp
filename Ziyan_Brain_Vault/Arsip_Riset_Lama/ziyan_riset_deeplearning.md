# Riset DeepLearning.AI — Kursus Gratis untuk Upskill Agent ZIYAN
Sumber: https://www.deeplearning.ai/courses/ (scrape katalog, verifikasi status "Free" per halaman kursus)
Tanggal: 2026-08-01 | Divisi Riset Mendalam ZIYAN

## Temuan Utama
- **Semua short course DeepLearning.AI GRATIS** (login email saja, tanpa kartu kredit). Yang berbayar hanya Specialization di Coursera (ML, DLS, GenAI with LLMs).
- Katalog memuat **±140 kursus**, ~40 di antaranya bertema agent/agentic/RAG/LLMOps.
- Hampir semua short course punya **notebook Jupyter** yang bisa di-download (materi terbuka), dan banyak yang mirror di GitHub partner (LangChain, CrewAI, LlamaIndex, Letta, HuggingFace smolagents, Anthropic MCP).
- Durasi standar short course: **1–2 jam** (beberapa "Agentic AI" oleh Andrew Ng lebih panjang, ±5 jam).

## Tabel Kursus Relevan

| Nama Kursus | Topik | Gratis? | Relevansi ZIYAN (1-5) | Manfaat konkret |
|---|---|---|---|---|
| Agentic AI (Andrew Ng) | 4 pola agentic: reflection, tool use, planning, multi-agent | Ya | 5 | Kerangka induk desain agent ZIYAN; bahasa netral framework → cocok dipasang di Hermes |
| Multi AI Agent Systems with crewAI | Role-based agent, task delegation, crew orchestration | Ya | 5 | Pola "divisi perusahaan" persis model ZIYAN (Orchestrator + divisi) |
| Practical Multi AI Agents & Advanced Use Cases with crewAI | Multi-agent produksi, guardrail, cost/latency | Ya | 5 | Upgrade divisi ZIYAN ke level produksi + kontrol biaya |
| AI Agents in LangGraph | State machine agent, loop, cycle, human-in-loop | Ya | 5 | Pola graf state → dipakai untuk workflow ZIYAN yang deterministik & bisa di-resume |
| Evaluating AI Agents | Tracing, eval trajectory, LLM-as-judge, metrik | Ya | 5 | Kualitas output divisi ZIYAN terukur; deteksi agent yang "ngawur" |
| AI Agentic Design Patterns with AutoGen | Conversational multi-agent, group chat, code exec | Ya | 4 | Pola debat/review antar-agent (mis. QA konten sebelum publish) |
| Building Agentic RAG with LlamaIndex | Router, tool retrieval, multi-doc agent | Ya | 4 | Riset kompetitor & knowledge base ZIYAN otomatis |
| LLMs as Operating Systems: Agent Memory (Letta/MemGPT) | Memory hierarchy, context paging | Ya | 5 | Memori jangka panjang ZIYAN tanpa DB berbayar |
| Long-Term Agentic Memory with LangGraph | Semantic/episodic/procedural memory | Ya | 4 | Agent belajar dari sesi lama (mirip skill Hermes) |
| Agent Memory: Building Memory-Aware Agents | Desain memori praktis | Ya | 4 | Pelengkap dua kursus memori di atas |
| Functions, Tools and Agents with LangChain | Function calling, tool schema, ReAct | Ya | 5 | Dasar tool-calling andal untuk model gratis 9router |
| MCP: Build Rich-Context AI Apps with Anthropic | Model Context Protocol, server tool | Ya | 4 | Standarisasi tool ZIYAN → plug-and-play antar agent |
| A2A: The Agent2Agent Protocol | Protokol komunikasi antar-agent | Ya | 3 | Referensi bila divisi ZIYAN jadi proses terpisah |
| Building Code Agents with HF smolagents | Code-as-action agent, sandbox | Ya | 4 | Agent eksekusi kode ringan, gratis, self-host |
| DSPy: Build & Optimize Agentic Apps | Optimasi prompt otomatis | Ya | 4 | Naikkan kualitas output model gratis tanpa ganti model |
| Building & Evaluating Advanced RAG | Sentence-window, reranking, RAG triad | Ya | 3 | Akurasi knowledge base ZIYAN |
| LLMOps | Pipeline, versioning, deploy | Ya | 3 | Disiplin operasional, tapi banyak bagian GCP (biaya) |
| Automated Testing for LLMOps | CI test untuk LLM app | Ya | 3 | Regression test skill/agent Hermes |
| Getting Structured LLM Output / Pydantic for LLM Workflows | JSON schema, validasi | Ya | 4 | Output antar-divisi ZIYAN valid & mesin-terbaca |
| Safe & Reliable AI via Guardrails | Guardrail, validator | Ya | 3 | Cegah agent publish konten bermasalah |
| Governing AI Agents | Kebijakan, kontrol, audit agent | Ya | 3 | Aturan main "perusahaan AI" ZIYAN |
| Semantic Caching for AI Agents | Cache jawaban, hemat token | Ya | 4 | Langsung menekan biaya/rate-limit model gratis |
| Building and Evaluating Data Agents | Agent analitik data | Ya | 3 | Divisi analitik/monetisasi berbasis data |
| Event-Driven Agentic Document Workflows | Workflow event-driven | Ya | 3 | Pola trigger otomatis (cron/webhook) untuk ZIYAN |
| Knowledge Graphs for AI Agent API Discovery | KG + tool discovery | Ya | 3 | Agent menemukan tool sendiri saat tool bertambah banyak |

## 5 Rekomendasi Prioritas

| # | Kursus | Alasan prioritas |
|---|---|---|
| 1 | **Agentic AI (Andrew Ng)** | Fondasi pola agentic paling netral & lengkap; jadi "kurikulum induk" sebelum yang lain. Langsung dipetakan ke skill Hermes. |
| 2 | **Multi AI Agent Systems with crewAI** (+ lanjutan Practical) | Arsitektur role/tugas/delegasi = cetak biru struktur divisi ZIYAN. Bisa ditiru tanpa install CrewAI. |
| 3 | **Evaluating AI Agents** | Tanpa evaluasi, agent otonom tidak bisa dipercaya untuk monetisasi. Memberi metrik & tracing trajectory. |
| 4 | **LLMs as Operating Systems: Agent Memory** | Memori persisten = syarat perusahaan yang jalan terus-menerus; solusi gratis/self-host. |
| 5 | **Functions, Tools and Agents with LangChain** | Tool-calling andal pada model gratis (9router/Gemini) adalah titik gagal utama ZIYAN saat ini. |

Cadangan bila ada waktu: **Semantic Caching for AI Agents** (hemat biaya langsung) dan **DSPy** (kualitas naik tanpa upgrade model).

## Catatan Implementasi untuk ZIYAN
- Notebook tiap kursus bisa di-download → simpan ke repo internal sebagai referensi pola, bukan dependency.
- Yang perlu API key berbayar (OpenAI di beberapa notebook) bisa diganti endpoint 9router/Gemini gratis (base_url override).
- Hindari kursus yang bergantung layanan berbayar (Vertex AI, Bedrock, Cerebras) kecuali hanya untuk konsep.
- Urutan belajar usulan: 1 → 5 → 2 → 4 → 3.
