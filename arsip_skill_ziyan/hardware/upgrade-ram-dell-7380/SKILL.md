---
name: upgrade-ram-dell-7380
description: Guide to upgrade RAM on the Dell Inspiron 7380 laptop.
---

# Upgrade RAM — Dell Inspiron 7380

Skill ini berisi fakta **terverifikasi via WMI** dari laptop Bos (bukan nebak):
- `Win32_ComputerSystem`: Maker = Dell Inc., Model = Inspiron 7380
- `Win32_PhysicalMemory`: 2 slot, terisi 2× 4 GB SK Hynix DDR4-2400MHz = 8 GB total
- Kedua slot **penuh** → tidak ada slot kosong

## Fakta Krucial (WAJIB paham sebelum beli)
| Item | Nilai |
|------|-------|
| Slot RAM | 2 (keduanya terisi) |
| Terpasang | 2× 4 GB = 8 GB, DDR4-2400MHz, SODIMM |
| Slot kosong | 0 |
| Jenis RAM | **SODIMM DDR4-2400** (laptop, BUKAN DIMM PC) |
| Max umum board ini | 16 GB (2× 8 GB) |

## Konsekuensi Desain
- **TIDAK BISA** tambah 1 stick → tidak ada slot kosong.
- **HARUS ganti 2 stick lama** dengan 2 stick baru (misal 2× 8 GB).
- Beli RAM kecepatan 2400MHz, atau 2666MHz (otomatis turun ke 2400).

## Rekomendasi Pembelian
- Ambil **2× 8 GB DDR4-2400 SODIMM** → total 16 GB.
- Cukup untuk jalanin LLM lokal ringan (llama3.2:1b, qwen2.5:3b) lancar.
- Hindari 2× 16 GB (32 GB) kecuali yakin board support & butuh berat.

## Estimasi Biaya (Pasar Indonesia, 2026)
| Opsi | Total | Harga |
|------|-------|-------|
| 2× 8 GB (16 GB) | 16 GB? | Rp 300.000 – 500.000 |
| 2× 16 GB (32 GB) | 32 GB | Rp 700.000 – 1.200.000 |
| Jasa pasang tukang servis | — | Rp 30.000 – 50.000 |

DDR4 murah karena generasi lama.

## Langkah Eksekusi
1. Beli 2 stick DDR4-2400 SODIMM (pastikan SODIMM, bukan DIMM).
2. Matikan laptop, cabut charger, tahan tombol power 10 dtk (buang sisa listrik).
3. Buka panel bawah (obeng Phillips kecil / kadang pry tool).
4. Lepas 2 stick 4 GB lama (tarik pengait samping → stick ngangkat → tarik).
5. Pasang 2 stick baru (masukkan miring 30°, tekan sampai pengait klik).
6. Tutup panel, nyalakan → cek Task Manager / Settings → harus baca 16 GB.

## Verifikasi Setelah Pasang
Jalankan di terminal (PowerShell):
```powershell
Get-CimInstance Win32_PhysicalMemory | ForEach-Object {
  "{0} GB | DDR{1} | {2} MHz" -f ([math]::Round($_.Capacity/1GB)), $_.SMBIOSMemoryType, $_.Speed
}
```
Harus muncul 2 baris @ 8 GB / DDR4 / 2400.

## Pitfall
- Salah beli DIMM (PC) → tidak masuk slot laptop.
- Beli 1 stick saja → tidak bisa pasang (slot penuh).
- Lupa buang sisa listrik → risk korslet komponen.
- Board 7380 umumnya max 16 GB; jangan beli 32 GB kalau tidak yakin.

## Kaitan dengan AI Lokal
Setelah 16 GB: Ollama bisa di-install ulang & jalanin model kecil offline.
Untuk 8 GB (sekarang): AI lokal tidak praktis — gunakan Hermes cloud (Nous) untuk tugas privat.
