# Windows Power Settings untuk 24/7 Always-On (ZIYAN)

## Masalah
Laptop Dell (Windows 11) sleep/lock screen → Hermes Gateway disconnect (Discord ack_stale, Telegram stop receiving). Proses gateway hidup tapi koneksi putus.

## Akar Masalah (Power Plan "Dell" default)
1. **Sleep after 15 menit** (STANDBYIDLE = 900s)
2. **Display off 10 menit** → trigger sleep
3. **PCIe ASPM = Maximum Power Savings** (index 2) → throttle network
4. **USB Selective Suspend = Enabled** → putus WiFi
5. **Wake Timers = Disabled** → scheduled task gak bisa wake

## Fix Permanen (PowerShell Admin)

### Opsi 1: Override scheme "Dell" (current)
```powershell
# Disable sleep/hibernate/hybrid sleep (AC & DC)
powercfg /setacvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setacvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setacvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0

# PCIe ASPM = Off
powercfg /setacvalueindex scheme_current SUB_PCIEXPRESS ASPM 0
powercfg /setdcvalueindex scheme_current SUB_PCIEXPRESS ASPM 0

# USB Selective Suspend = Disabled
powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

# Wake Timers = Enable
powercfg /setacvalueindex scheme_current SUB_SLEEP RTCWAKE 1
powercfg /setdcvalueindex scheme_current SUB_SLEEP RTCWAKE 1

# Apply
powercfg /setactive scheme_current
```

### Opsi 2: Aktifkan High Performance Scheme (Quick Fix)
```powershell
# Duplicate High Performance scheme
powercfg /duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
# Activate it
powercfg /setactive f8bf9830-1d5e-4187-a347-96873927865b
```

## Verifikasi
```powershell
# Check active scheme
powercfg /getactivescheme

# Verify key settings
powercfg /query scheme_current | findstr /i "STANDBYIDLE HIBERNATEIDLE HYBRIDSLEEP ASPM RTCWAKE"
```

Expected values (AC):
- STANDBYIDLE = 0x00000000 (Never sleep)
- HIBERNATEIDLE = 0x00000000 (Never hibernate)
- HYBRIDSLEEP = 0x00000000 (Off)
- ASPM = 0x00000000 (Off)
- RTCWAKE = 0x00000001 (Enable)

## Tambahan: Scheduled Task + Cron untuk Gateway Supervision

### Scheduled Task: `Hermes_Gateway_Auto`
- Trigger: Daily, repeat every 30 minutes (survives sleep/wake)
- Action: `cmd /c "C:\Users\arija\ZIYAN_BRIDGE\start_n8n.bat"` (or gateway start)

### Cron Job: `Hermes_Gateway_Health` (5 menit)
```bash
# Check process + Discord WebSocket → restart kalau mati
# Di hermes cron jobs
```

## Catatan
- Display off OK (10 menit AC, 5 menit DC) — screen bisa mati, tapi jangan sleep
- High Performance scheme sudah default disable sleep, tapi verify PCIe ASPM & USB suspend
- Windows 11 Modern Standby (S0ix) masih bisa potong network — disable via power settings di atas
- Test: lock screen (Win+L) → wait 20 menit → cek Discord/Telegram masih terima pesan