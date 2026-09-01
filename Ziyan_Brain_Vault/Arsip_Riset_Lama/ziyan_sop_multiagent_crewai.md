# SOP Struktur Organisasi Multi-Agent ZIYAN
**Referensi:** DeepLearning.AI — *Multi AI Agent Systems with crewAI* (João Moura, crewAI CEO)
**Status:** Ringkas & actionable | **Bahasa:** Indonesia
**Catatan:** ZIYAN TIDAK pakai crewAI. Kita *replika* konsep crew (role + task + delegasi) ke `delegate_task` Hermes + skills.

---

## 1. Konsep Inti crewAI (Ringkasan)

| Konsep | Fungsi | Atribut kunci |
|--------|--------|---------------|
| **Agent** | Unit otonom spesialis | `role` (fungsi), `goal` (tujuan), `backstory` (konteks/persona), `tools`, `allow_delegation`, `llm` |
| **Task** | Satu assignment spesifik | `description`, `expected_output`, `agent`, `tools`, `context` (output task lain sebagai input) |
| **Process** | Strategi eksekusi | `sequential` (berurutan), `hierarchical` (ada manager yang bagi tugas), `parallel` (bersamaan) |
| **Crew** | Kumpulan agents + tasks + process | `agents`, `tasks`, `process`, `memory`, `verbose`, `manager_llm` |
| **Memory** | Ingatan antar agent | short-term, long-term, shared/entity memory (skrg API `Memory` unified) |
| **Collaboration** | Delegasi & tanya antar agent | `allow_delegation=True` → agent bisa delegasikan sub-tugas & tanya rekan |
| **Flows** | Orkestrasi lintas crew | event-driven, manage state, rangkai beberapa crew/task jadi workflow besar |
| **Tools** | Kapabilitas agent | pre-built (search, scrape) + custom tools |

**6 business process dari course** (template reusable): resume tailor, riset+tulis+edit artikel, customer support, customer outreach, event planning, financial analysis.

**Prinsip kunci course:** Role-playing → Memory → Tools → Focus (breakdown tugas) → Guardrails (error/hallucination/loop) → Cooperation (series/parallel/hierarchical).

---

## 2. Mapping crewAI → ZIYAN (Bentuk "Divisi" via delegate_task + skills)

ZIYAN = perusahaan 100% AI agent. Infra: **Hermes Orchestrator** (manager), **delegate_task** (delegasi), **skills** (toolkit/role-kit), **9router gratis + Gemini key** (LLM), **computer_use**, **session_search** (memory jangka panjang).

| crewAI | Padanan ZIYAN | Cara implementasi |
|--------|---------------|-------------------|
| Agent (role/goal/backstory) | **Divisi** | Satu skill = satu divisi. `role`+`goal`+`backstory` dijadikan system prompt skill (FRONTMATTER + instruksi). Contoh: `divisi-riset-mendalam`, `divisi-content-intel`, `ziyan-video-production`, `ziyan-ai-infra`. |
| Tools | **Skills + tools Hermes** | Skills = toolkit spesialis (web, arxiv, youtube, p5js, comfyui, dll). Tools native: `terminal`, `browser_*`, `computer_use`, `search_files`. |
| Task | **Satu delegate_task call** | Orchestrator panggil `delegate_task(subagent, brief)`. `description` = brief; `expected_output` = format hasil; `context` = output divisi sebelumnya yang di-pass ke brief berikutnya. |
| Process sequential | **Delegasi berantai** | Output Divisi A dimasukkan ke brief Divisi B → C → D. |
| Process hierarchical | **Orchestrator = manager_llm** | Hermes pecah goal besar → delegate ke leaf subagent per divisi → kumpulkan & sintesis. Sama persis dengan `manager_llm`/`manager_agent` crewAI. |
| Process parallel | **Beberapa delegate_task bersamaan** | Kampanye besar: Riset + Video + Outreach dijalankan paralel, lalu Orchestrator gabung. |
| Crew | **Satu "Kampanye/Proyek"** | Kumpulan delegate_task + flow yang dijalankan Orchestrator untuk 1 objective (mis. "launch video ZIYAN mingguan"). |
| Memory | **session_search + file SOP + skill memory** | Short-term = konteks sesi; Long-term = file `ziyan_sop_*.md` + skill memory; Shared = satu file memory/state yang dibaca banyak divisi. |
| allow_delegation | **delegate_task (rekursif)** | Divisi boleh minta Orchestrator delegate sub-tugas ke divisi lain (mis. Content Intel delegate riset ke Divisi Riset). |
| Flows | **SOP / playbook file** | File ini + `company-playbook` = definition flow orkestrasi lintas divisi. |

### Divisi ZIYAN & skill pendukungnya
- **Divisi Riset** → skill `divisi-riset-mendalam`, `arxiv`, `web`, `youtube-content`, `blogwatcher`
- **Content Intel** → skill `divisi-content-intel` (bedah kompetitor), `humanizer`, `baoyu-infographic`
- **Video Production** → skill `ziyan-video-production`, `notebooklm-video`, `comfyui`, `manim-video`, `p5js`
- **Outreach** → skill `hermes-messaging-gateway` (Discord/Telegram/WhatsApp), `company-playbook`
- **Infra / AI** → skill `ziyan-ai-infra`, `llm-proxy-9router`, `huggingface-hub`, `autonomous-ai-agents`

---

## 3. SOP Struktur Organisasi ZIYAN

### 3.1 Hirarki (Hierarchical Process)
```
            [HERMES ORCHESTRATOR]  ← manager_llm (Bos / user)
                         │ delegate_task
   ┌──────────┬──────────┼──────────┬──────────┐
   ▼          ▼          ▼          ▼          ▼
DIVISI   CONTENT     VIDEO      OUTREACH    INFRA
RISET    INTEL       PRODUCTION             / AI
```
- Orchestrator SATU-SATUNYA yang pegang goal akhir & membagi tugas. Divisi TIDAK komunikasi langsung antar sesi — semua lewat Orchestrator (mirip `manager_agent`).
- Setiap divisi = 1 subagent dengan 1 skill ter-loaded. Brief wajib berisi: objective, input/context, format output, batas (guardrails).

### 3.2 Kapan SEQUENTIAL vs PARALLEL

**SEQUENTIAL (berantai) — pakai bila ada ketergantungan data:**
- Pipeline konten: Riset → Content Intel (olah) → Video Production (render) → Outreach (sebar).
- Aturan: output divisi N **harus** jadi `context` brief divisi N+1.
- Guardrail: tiap tahap wajib `expected_output` jelas agar tahap berikutnya tidak kehilangan input.

**PARALLEL (bersamaan) — pakai bila independen:**
- Riset tren (Divisi Riset) + riset kompetitor (Content Intel) + draft aset (Video) dijalankan bersama di awal kampanye.
- Outreach multi-channel (Telegram + WhatsApp + Discord) bisa paralel.
- Orchestrator gabung hasil paralel di tahap sintesis akhir.

**HIERARCHICAL (selalu) — Orchestrator sebagai manajer:**
- Goal kompleks selalu dipecah Orchestrator → delegate ke leaf. Leaf TIDAK spawn divisi lain; kalau butuh, kembalikan ke Orchestrator (rekursi via `delegate_task`).

### 3.3 Template Brief delegate_task (standar tiap divisi)
```
ROLE: <Divisi X>
GOAL: <hasil spesifik & terukur>
CONTEXT: <output dari divisi sebelumnya / link / file>
CONSTRAINTS: <jangan print key, bahasa ID, max N kata, dll>
EXPECTED_OUTPUT: <format: tabel / markdown / file path>
ESCALATION: <kalau gagal, return ke Orchestrator, jangan retry himself>
```

### 3.4 Memory Antar Agent (replika shared memory crewAI)
- **Short-term:** konteks dalam 1 sesi delegate_task.
- **Long-term:** simpan hasil penting ke `C:\Users\arija\ziyan_*.md`; baca via `read_file` di sesi berikutnya.
- **Shared state:** 1 file `ziyan_state.md` (atau SOP) yang jadi rujukan semua divisi (brand voice, target, jadwal).
- **Procedural:** skill = ingatan cara kerja tiap divisi (skill_manage patch bila perlu update).
- **Recall:** sebelum mulai, Orchestrator jalan `session_search` untuk konteks lintas sesi.

### 3.5 Guardrails (wajib, dari prinsip course)
- Max iterasi & timeout per task → set `timeout` di terminal/process.
- Anti-hallucination: divisi wajib cantumkan sumber (url/file) di output.
- Anti-loop: Orchestrator batasi max 1 level delegasi rekursif; leaf kembalikan ke Orchestrator bila mandek.
- Secret: **jangan pernah print API key / Gemini key** di output chat.

---

## 4. TABEL: Konsep crewAI | Padanan di ZIYAN | Catatan Implementasi

| Konsep crewAI | Padanan di ZIYAN | Catatan implementasi |
|---------------|------------------|----------------------|
| **Agent** (`role`/`goal`/`backstory`) | Divisi (1 skill = 1 role) | Tulis role/goal/backstory di FRONTMATTER + instruksi skill. Mis. `divisi-content-intel`. |
| **Tools** | Skills + tools Hermes | Setiap skill = toolkit spesialis. Load via `skill_view` sebelum delegate. |
| **Task** | 1x `delegate_task` | Brief = description; format = expected_output; hasil sebelumnya = context. |
| **Task.context** | Pass output antar brief | Output Divisi A di-copy ke brief Divisi B (sequential). |
| **Process.sequential** | Delegasi berantai | Riset→Content→Video→Outreach; tiap tahap dependency data. |
| **Process.hierarchical** | Orchestrator = manager | Hermes pecah goal → delegate leaf → sintesis. Max 1 level rekursi. |
| **Process.parallel** | Multi `delegate_task` bersamaan | Tugas independen (riset + aset + outreach channel) dijalankan paralel. |
| **Crew** | 1 Kampanye/Proyek | Kumpulan delegate_task + flow untuk 1 objective bisnis. |
| **Memory (short/long/shared)** | session_search + file SOP + skill memory | Simpan ke `ziyan_*.md`; rujukan lintas sesi via `read_file`/`session_search`. |
| **allow_delegation** | `delegate_task` rekursif | Leaf minta Orchestrator delegate sub-tugas, bukan spawn sendiri. |
| **Flows** | SOP / `company-playbook` | File ini mendefinisikan orkestrasi lintas divisi (event/state). |
| **Manager LLM** | Hermes Orchestrator (Bos) | Satu otoritas bagi & kumpulkan tugas. |
| **Guardrails** | Constraint di brief + timeout | Max iter, cantumkan sumber, jangan print key, batasi rekursi. |
| **Verbose** | `verbose`/`notify_on_complete` | Log tiap tahap; bg process wajib `notify_on_complete`. |

---

## 5. Checklist Cepat (Cheat Sheet)
- [ ] Tentukan **goal** & pecah jadi task (sequential/parallel?).
- [ ] Pilih **divisi/skill** yang cocok tiap task.
- [ ] Tulis **brief standar** (role/goal/context/constraints/output).
- [ ] Jalankan: sequential = berantai; parallel = bersamaan; hierarchical = selalu lewat Orchestrator.
- [ ] Simpan hasil ke **file SOP/state** untuk memory lintas sesi.
- [ ] **Jangan print key.** Cantumkan sumber. Batasi rekursi delegasi = 1 level.

*Sumber: docs.crewai.com (Agents, Tasks, Crews, Processes, Memory, Collaboration, Flows) + deeplearning.ai course outline "Multi AI Agent Systems with crewAI".*
