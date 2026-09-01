# SOP: Agent QC & Evaluasi ZIYAN
Basis: DeepLearning.AI — "Evaluating AI Agents" (Arize AI / Phoenix). Versi 1.0.

---

## 1. Ringkasan Metode Evaluasi Agent (materi publik kursus)

Kursus ini membagi evaluasi agent jadi 4 lapis:

**A. Tracing (jejak eksekusi)**
- Setiap agent run = 1 **trace**; tiap langkah = **span** (LLM call, tool call, retriever, router).
- Span wajib punya: input, output, latency, token/biaya, status (ok/error).
- Tanpa tracing, evaluasi mustahil — kamu cuma lihat output akhir, bukan penyebab gagal.

**B. Evaluasi per-komponen (component-level)**
- **Router eval**: apakah agent pilih skill/tool yang benar untuk intent user?
- **Tool-correctness**: tool yang dipanggil benar? argumen/parameter benar? urutan benar?
- **Faithfulness / groundedness**: jawaban didukung data yang benar-benar diambil (tidak halu).
- **Relevance**: output menjawab pertanyaan yang diminta.
- Alat: **LLM-as-a-judge** dengan template eval (label + *explanation* wajib, bukan skor angka telanjang).

**C. Trajectory evaluation (path-level)**
- Bandingkan urutan langkah aktual vs **golden/reference trajectory**.
- Metrik: convergence (jumlah langkah untuk selesai), loop detection, dead-end, langkah mubazir.
- Agent bisa benar hasilnya tapi buruk jalurnya (boros token/waktu) → tetap gagal QC.

**D. Evaluasi end-to-end (outcome)**
- Task completion / goal achievement.
- Biaya & latency per task.
- Human feedback / annotation queue untuk kasus ambigu.

**Prinsip kunci kursus:**
1. Bangun **dataset eval** (kumpulan kasus + expected output) sebelum optimasi apa pun.
2. Eval harus **otomatis + berulang** (regression test tiap kali prompt/tool diubah).
3. **Benchmark dulu, baru iterasi** — ubah 1 variabel per eksperimen.
4. LLM-judge harus **dikalibrasi** ke label manusia dulu sebelum dipercaya.

---

## 2. Pemetaan ke Infrastruktur ZIYAN

| Konsep kursus | Padanan di ZIYAN |
|---|---|
| Trace | 1 `delegate_task` = 1 trace sub-agent |
| Span | Tiap tool call dalam live transcript sub-agent |
| Trace store / Phoenix | `ZIYAN_COMPANY_LOG` (append-only, timestamp + divisi + task id) |
| Golden trajectory | SOP divisi (skill file) = jalur referensi |
| LLM-as-judge | Orchestrator (atau agent QC terpisah, model 9router gratis) menilai transcript |
| Outcome metric | Revenue, task completion, deliverable diterima klien |
| Annotation queue | Review manual Bos untuk kasus flagged |

**Aturan audit sub-agent:**
- Orchestrator **wajib baca live transcript**, bukan cuma summary sub-agent. Summary bisa bohong/optimistis.
- Klaim tanpa bukti tool output = **fabrikasi** → tolak, jangan lapor ke Bos.
- Setiap file deliverable harus diverifikasi ada di disk (cek path), bukan diasumsikan.
- Log ke `ZIYAN_COMPANY_LOG`: task, divisi, durasi, status, biaya (token/model), verdict QC.

**Metrik sukses ZIYAN (urut prioritas):**
1. **Revenue / prospek konversi** (outcome sejati)
2. **Task completion rate** — deliverable nyata & terverifikasi
3. **Tool-correctness rate** — % sub-agent pakai tool/skill benar
4. **Faithfulness rate** — % klaim yang punya bukti tool output
5. **Efficiency** — jumlah langkah & token per task vs baseline
6. **Rework rate** — % hasil yang harus diulang setelah QC

---

## 3. CHECKLIST QC — sebelum hasil diserahkan ke Bos / Klien

### Gate 0 — Kelengkapan (fail = balikin ke sub-agent)
- [ ] Semua deliverable yang diminta ada? (hitung 1:1 vs instruksi)
- [ ] File tersimpan di path yang benar dan **terverifikasi ada** (cek listing/read).
- [ ] Format sesuai permintaan (bahasa, panjang, tabel, tidak dikirim ke chat jika dilarang).

### Gate 1 — Faithfulness (anti-halusinasi)
- [ ] Setiap angka, harga, nama, URL, statistik → ada sumber/tool output di transcript?
- [ ] Tidak ada output tool yang **dikarang** (data palsu pengganti fetch gagal).
- [ ] Kalau ada blocker (network/API gagal), dilaporkan jujur — bukan ditutupi.
- [ ] Tidak ada key/credential/secret yang bocor di output atau file.

### Gate 2 — Tool-correctness
- [ ] Tool/skill yang dipakai memang yang tepat (bukan reinvent manual).
- [ ] Skill divisi relevan sudah di-load sebelum eksekusi.
- [ ] Tidak ada tool call error yang diabaikan diam-diam.

### Gate 3 — Trajectory
- [ ] Tidak ada loop / pengulangan langkah sama >2x.
- [ ] Jumlah langkah wajar vs SOP referensi (tandai jika >2x baseline).
- [ ] Tidak ada langkah destruktif tanpa izin (hapus file, kirim pesan, transaksi).

### Gate 4 — Kualitas bisnis
- [ ] Actionable: ada langkah berikut yang jelas, bukan cuma teori.
- [ ] Sesuai brand & bahasa ZIYAN (Bahasa Indonesia, ringkas, tanpa AI-isms).
- [ ] Untuk klien: bebas typo, bebas jejak internal (nama agent, path lokal, log debug).
- [ ] Nilai jual jelas — apa yang klien dapat, kenapa layak dibayar.

### Gate 5 — Logging & pelaporan
- [ ] Entry `ZIYAN_COMPANY_LOG` ditulis: task id, divisi, durasi, status, verdict.
- [ ] Laporan ke Bos: outcome dulu, lalu bukti, lalu blocker. Maks ringkas.
- [ ] Kalau ada Gate gagal → **jangan lapor sukses**. Lapor status parsial + rencana perbaikan.

**Aturan keras:** ≥1 item Gate 1 gagal = **BLOK TOTAL**. Hasil tidak boleh keluar ke Bos/klien.

---

## 4. Ritme Evaluasi (cadence)

| Frekuensi | Aktivitas |
|---|---|
| Tiap task | Checklist Gate 0–5 oleh Orchestrator |
| Mingguan | Rekap `ZIYAN_COMPANY_LOG`: completion rate, rework rate, biaya per task |
| Tiap ubah skill/prompt | Regression: jalankan ulang 3–5 task golden, bandingkan hasil |
| Bulanan | Kalibrasi: Bos review 10 transcript acak, cocokkan dengan verdict QC agent |

**Dataset eval ZIYAN (bangun bertahap):** simpan 10–20 task historis + hasil ideal sebagai golden set untuk regression test tiap kali infra/model diganti (mis. pindah model 9router).

---

## 5. Tabel Ringkas

| Metode Eval | Implementasi ZIYAN | Trigger Penggunaan |
|---|---|---|
| **Tracing** | Baca live transcript `delegate_task` penuh; arsip ke `ZIYAN_COMPANY_LOG` | Setiap delegasi sub-agent, tanpa kecuali |
| **Tool-correctness** | Cek tool & skill yang dipanggil vs SOP divisi | Tiap task yang pakai tool eksternal (web, computer_use, file) |
| **Faithfulness / groundedness** | Tiap klaim harus punya bukti tool output di transcript | Riset, data pasar, harga, statistik, laporan klien |
| **Trajectory eval** | Bandingkan urutan langkah vs SOP; deteksi loop & langkah mubazir | Task >10 langkah, atau task gagal/lambat |
| **Router eval** | Apakah Orchestrator pilih divisi/skill yang tepat | Saat rework rate naik atau task salah sasaran |
| **LLM-as-judge** | Agent QC terpisah (model gratis 9router) nilai draft sebelum kirim | Deliverable klien, konten publikasi, proposal |
| **Task completion** | Verifikasi file/aset benar-benar ada & sesuai spesifikasi | Setiap penutupan task |
| **Cost & latency** | Catat token/model/durasi per task | Rekap mingguan; sebelum ganti model |
| **Regression test** | Jalankan ulang golden set 3–5 task | Setiap ubah prompt, skill, atau model |
| **Human annotation** | Bos review sampel transcript acak | Bulanan, atau saat verdict QC diragukan |
| **Outcome / revenue** | Lacak konversi prospek → bayar | Review mingguan & bulanan |
