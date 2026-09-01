# Windows 11 Power Management Fix for 24/7 Gateway Operation

## Problem
Hermes gateway (Discord + Telegram) goes offline when laptop screen turns off/locks. Network adapter sleeps, WebSocket disconnects.

## Root Causes (Windows 11, Dell laptop, 8GB RAM)
1. **Sleep after 15 min** (STANDBYIDLE = 900s)
2. **Display off 10 min** → triggers sleep
3. **PCIe ASPM = Maximum Power Savings** → throttles network
4. **USB Selective Suspend = Enabled** → can cut WiFi USB
5. **Wake Timers = Disabled** → scheduled tasks can't wake laptop
6. **Modern Standby (S0ix)** → network drops on lock screen

## Fix Applied (PowerShell commands, run as admin)

```powershell
# 1. Disable sleep entirely (AC & DC)
powercfg /setacvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0

# 2. Disable hibernate
powercfg /setacvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0

# 3. Disable hybrid sleep
powercfg /setacvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0

# 4. PCIe ASPM = Off (prevent network throttle)
powercfg /setacvalueindex scheme_current SUB_PCIEXPRESS ASPM 0
powercfg /setdcvalueindex scheme_current SUB_PCIEXPRESS ASPM 0

# 5. USB Selective Suspend = Disabled
powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

# 6. Wake Timers = Enable
powercfg /setacvalueindex scheme_current SUB_SLEEP RTCWAKE 1
powercfg /setdcvalueindex scheme_current SUB_SLEEP RTCWAKE 1

# 7. Apply changes
powercfg /setactive scheme_current
```

## Better: Switch to High Performance Scheme
```powershell
# Duplicate High Performance scheme
powercfg /duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
# Activate it
powercfg /setactive f8bf9830-1d5e-4187-a347-96873927865b
```

## Verification
```powershell
# Check actual values
powercfg /query scheme_current | findstr /i "STANDBYIDLE HIBERNATEIDLE HYBRIDSLEEP ASPM RTCWAKE"
# Should show: STANDBYIDLE=0, HIBERNATEIDLE=0, HYBRIDSLEEP=0, ASPM=0, RTCWAKE=1
```

## Additional: Prevent Network Adapter Sleep
```powershell
# Check current adapter power management
Get-NetAdapter | Where-Object Status -eq 'Up' | ForEach-Object {
    Get-NetAdapterPowerManagement -Name $_.Name
}

# If PowerSavings=True, disable via Device Manager or:
# (Requires admin) Set-NetAdapterPowerManagement -Name "Wi-Fi" -PowerSavings $false
```

## Result
- Laptop screen can turn off (10 min)
- **No sleep, no hibernate, no hybrid sleep**
- Network stays active 24/7
- Gateway WebSocket stays connected
- Scheduled tasks (cron, n8n) run reliably

## Related
- `references/n8n_windows_startup.md` - n8n auto-start on Windows
- `references/9router_auto_start.md` - 9Router auto-start via Startup folder