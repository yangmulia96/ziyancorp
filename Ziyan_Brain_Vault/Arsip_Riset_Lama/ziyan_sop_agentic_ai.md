# SOP ZIYAN — Agentic AI (Andrew Ng / DeepLearning.AI)

Sumber: seri "Agentic Design Patterns" Andrew Ng (The Batch, DeepLearning.AI) + kursus *Agentic AI*.
Prinsip inti: **GPT-3.5 dengan agentic workflow mengalahkan GPT-4 zero-shot** (HumanEval). Artinya: model gratis (gemma/nemotron di 9router) + workflow bagus > model mahal tanpa workflow. Ini fondasi ekonomi ZIYAN.

Kita **TIDAK pakai LangGraph/CrewAI/AutoGen**. Kita replika 4 pola ke sistem skill + `delegate_task` Hermes.

---

## 1. REFLECTION (Refleksi)

**Inti kursus:** Agent memeriksa hasil kerjanya sendiri, mengkritik, lalu merevisi. Varian kuat = *self-reflection* (agent yang sama, prompt kritik terpisah) dan *external feedback* (unit test, linter, agent kedua sebagai kritikus). Loop: Draft → Critique → Revise (1–3 iterasi, berhenti kalau kritik sudah kosmetik).

**Implementasi ZIYAN via Hermes:**
- GM (saya) tidak pernah kirim output sub-agent mentah ke Bos.
- Pola: sub-agent A produksi draft → sub-agent B (reviewer, model berbeda) kritik → A revisi → GM approve.
- Feedback eksternal murah: jalankan skill/tool nyata (cek link hidup via curl, cek file benar-benar ada, jalankan kode) — bukan cuma opini LLM.

**SOP Reflection:**
1. Tentukan **kriteria lulus** SEBELUM kerja (3–5 poin terukur: faktual, panjang, format, CTA, bahasa).
2. Delegate task produksi → sub-agent A.
3. Delegate task review → sub-agent B dengan prompt kritikus (di bawah). Gunakan model berbeda dari A agar bias tidak sama.
4. Jika skor < ambang (mis. 8/10), kirim balik ke A dengan daftar perbaikan konkret. Maks **2 putaran**.
5. Verifikasi objektif (file ada? link 200? angka cocok?) — WAJIB, bukan opsional.
6. Baru lapor ke Bos, sertakan 1 baris "sudah direview oleh <reviewer>, skor X/10".

**Contoh prompt reviewer:**
```
Role: reviewer independen. JANGAN memuji.
Kriteria lulus: (1) fakta punya sumber, (2) bahasa Indonesia natural non-AI,
(3) <= 300 kata, (4) ada CTA, (5) tidak ada klaim yang tak bisa diverifikasi.
Output WAJIB format:
SKOR: n/10
PELANGGARAN: - kriteria# : kutipan masalah : perbaikan konkret
VERDICT: LULUS | REVISI
```

---

## 2. TOOL USE (Penggunaan Alat)

**Inti kursus:** LLM memanggil fungsi eksternal (web search, code exec, API, DB, vision) untuk hal yang tidak bisa/tidak boleh dihalusinasi. Kunci: deskripsi tool yang jelas, jumlah tool dibatasi & relevan (retrieval tool kalau banyak), dan hasil tool dikembalikan ke konteks untuk penalaran lanjutan.

**Implementasi ZIYAN via Hermes:**
- Tool = `terminal`, `write_file`, `search_files`, `browser_*`, `computer_use`, `vision_analyze`, `text_to_speech`.
- **Skill = tool level-2**: prosedur tersimpan (`ziyan-ai-infra`, `divisi-content-intel`, `notebooklm-video`, `llm-proxy-9router`). Skill adalah "tool yang berisi SOP", lebih murah daripada re-reasoning tiap kali.
- Aturan: apa pun yang bisa diverifikasi mesin (harga, tanggal, isi file, status API) HARUS lewat tool, bukan ingatan model.

**SOP Tool Use:**
1. Sebelum menjawab, tanya: "apakah klaim ini bisa dicek mesin?" Kalau ya → panggil tool.
2. Cek skill dulu (`skills_list`) sebelum bikin cara baru. Skill > improvisasi.
3. Batch panggilan tool yang independen dalam satu giliran (hemat context & waktu).
4. Setelah tool gagal: jangan mengarang hasil. Laporkan blocker + coba jalur alternatif (9router → Gemini key → browser).
5. Jika sebuah prosedur berhasil setelah ≥5 tool call → simpan jadi skill baru (`skill_manage`).
6. Jangan pernah print API key ke output/chat.

**Struktur delegasi dengan tool eksplisit:**
```
TASK: <tujuan 1 kalimat>
TOOLS WAJIB: terminal(curl), write_file
SKILL YANG HARUS DILOAD: ziyan-ai-infra
LARANGAN: jangan tebak angka, semua data dari curl
OUTPUT: file di C:\Users\arija\<nama>.md + ringkasan 5 bullet
```

---

## 3. PLANNING (Perencanaan)

**Inti kursus:** Agent memecah tujuan besar jadi urutan sub-task dan memilih tool/urutan sendiri (mis. ReAct, "Chain-of-Thought as planning"). Ng menekankan planning powerful tapi **kurang bisa diprediksi** — pakai kalau alur tidak bisa di-hardcode; kalau alur sudah jelas, tulis workflow deterministik saja.

**Implementasi ZIYAN via Hermes:**
- GM WAJIB bikin `todo` list sebelum delegate apa pun yang ≥3 langkah.
- Dekomposisi: 1 sub-agent = 1 deliverable jelas = 1 file/artefak. Jangan kasih task kabur.
- Alur rutin (produksi konten, riset kompetitor) → jadikan **skill deterministik**, bukan planning ad-hoc. Hemat token & konsisten.

**SOP Planning:**
1. Tulis **Definition of Done** dalam 1 kalimat (artefak apa, di mana).
2. Pecah jadi sub-task atomik; tandai mana yang **paralel** (tak saling bergantung) dan mana **serial**.
3. Petakan tiap sub-task → sub-agent + skill + tool + path output.
4. Tentukan budget: maks tool call / maks putaran revisi.
5. Simpan rencana ke `todo` (satu item `in_progress`, sisanya `pending`).
6. Eksekusi: paralel dulu (batch delegate), serial menyusul.
7. Review terhadap Definition of Done, bukan terhadap "kelihatan bagus".

**Template rencana:**
```
GOAL: <hasil akhir>
DONE WHEN: <file/artefak konkret>
[P] A. riset sumber      -> subagent-riset  -> riset.md
[P] B. bedah kompetitor  -> subagent-intel  -> intel.md
[S] C. sintesis A+B      -> subagent-writer -> draft.md
[S] D. review + revisi   -> subagent-review -> final.md
BUDGET: 4 agent, maks 2 putaran revisi
```

---

## 4. MULTI-AGENT COLLABORATION

**Inti kursus:** Beberapa agent dengan **peran berbeda** (planner, coder, tester, kritikus) berkolaborasi. Manfaat: spesialisasi prompt, konteks terfokus, dan kualitas naik lewat debat/pembagian kerja — mirip tim manusia. Risiko: biaya & chatter berlebihan.

**Implementasi ZIYAN via Hermes:**
- GM = orchestrator; sub-agent = divisi (Riset Mendalam, Content Intel, Produksi Video, Infra).
- Paralel: kirim beberapa `delegate_task` sekaligus untuk task independen → waktu jam jadi menit.
- Tiap sub-agent leaf: konteks minimum + path kerja + format output baku, supaya hasil bisa digabung.
- Model berbeda per peran (gemma untuk drafting, nemotron/Gemini untuk review) = "keragaman opini" gratis.

**SOP Multi-Agent:**
1. Definisikan peran + 1 kalimat mandat per agent (hindari 2 agent kerja tumpang tindih).
2. Kirim task independen **dalam satu batch paralel**.
3. Setiap prompt delegasi wajib memuat: ROLE, TASK, CONTEXT seperlunya, TOOLS, OUTPUT PATH, FORMAT, LARANGAN.
4. Jangan biarkan sub-agent saling ngobrol bebas — semua sinkronisasi lewat GM (hub-and-spoke). Hemat token, anti-loop.
5. Gabungkan hasil: GM sintesis, bukan copy-paste tempel.
6. Lewatkan hasil gabungan ke pola Reflection sebelum ke Bos.
7. Catat agent mana yang sering gagal → perbaiki skill-nya, bukan ulangi prompt yang sama.

**Contoh prompt delegasi baku:**
```
ROLE: leaf agent, Divisi <X>
TASK: <1 kalimat>
CONTEXT: ZIYAN, infra Hermes + 9router gratis. Jangan pakai framework eksternal.
TOOLS: <daftar>   SKILL: <nama skill>
WORKSPACE: C:\Users\arija
OUTPUT: tulis ke <path>. JANGAN kirim isi file ke chat.
FORMAT: Bahasa Indonesia, ringkas, actionable, ada tabel penutup.
LARANGAN: tidak mengarang data; tidak print API key.
```

---

## Aturan Gabungan (cara 4 pola ini dipakai bareng)

Planning → Multi-Agent (paralel) → Tool Use (di tiap agent) → Reflection (gate terakhir) → lapor Bos.
Berhenti kalau: kriteria lulus tercapai ATAU budget putaran habis (lapor apa adanya, jangan dipaksa).

---

## Tabel Status

| Pola | Implementasi di ZIYAN | Status |
|---|---|---|
| Reflection | Sub-agent reviewer (model beda) + verifikasi objektif sebelum lapor Bos | Belum ada — reviewer masih manual/ad-hoc, perlu skill `ziyan-reviewer` |
| Tool Use | terminal/curl, write_file, browser, computer_use, vision, edge-tts, flux + skill library | Sudah ada |
| Planning | `todo` + Definition of Done + peta paralel/serial sebelum delegate | Sebagian — sering dilewati untuk task kecil, perlu dijadikan wajib ≥3 langkah |
| Multi-Agent | `delegate_task` paralel ke divisi (Riset, Content Intel, Video, Infra), hub-and-spoke via GM | Sudah ada |
| Model diversity (pendukung) | gemma draft / nemotron-Gemini review via 9router | Sebagian — belum ada aturan baku mapping model→peran |

**Aksi berikutnya (prioritas):**
1. Bikin skill `ziyan-reviewer` (prompt kritikus + rubrik skor) — menutup gap Reflection.
2. Tambah aturan wajib `todo` untuk task ≥3 langkah di playbook GM.
3. Tulis mapping baku model→peran di skill `ziyan-ai-infra`.
