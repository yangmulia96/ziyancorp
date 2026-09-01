# Power Management Commands for 24/7 Windows AI Agents

## Quick Apply (Run as Admin)
```powershell
# High Performance scheme
powercfg /setactive f8bf9830-1d5e-4187-a347-96873927865b

# Disable sleep/hibernate
powercfg /setacvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP STANDBYIDLE 0
powercfg /setacvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HIBERNATEIDLE 0
powercfg /setacvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0
powercfg /setdcvalueindex scheme_current SUB_SLEEP HYBRIDSLEEP 0

# Network adapter (WiFi)
powercfg /setacvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0
powercfg /setdcvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0

# PCIe ASPM Off
powercfg /setacvalueindex scheme_current SUB_PCIEXPRESS ASPM 0
powercfg /setdcvalueindex scheme_current SUB_PCIEXPRESS ASPM 0

# USB Selective Suspend
powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

# Wake timers
powercfg /setacvalueindex scheme_current SUB_SLEEP RTCWAKE 1
powercfg /setdcvalueindex scheme_current SUB_SLEEP RTCWAKE 1

# Apply
powercfg /setactive scheme_current
```

## Verify
```powershell
powercfg /query scheme_current | findstr /i "STANDBYIDLE HIBERNATEIDLE HYBRIDSLEEP ASPM RTCWAKE"
```

## GUID Reference
| Setting | Subgroup GUID | Setting GUID |
|---------|---------------|--------------|
| Sleep after | 238c9fa8-0aad-41ed-83f4-97be242c8f20 | 29f6c1db-86da-48c5-9fdb-f2b67b1f44da |
| Hibernate after | 238c9fa8-0aad-41ed-83f4-97be242c8f20 | 9d7815a6-7ee4-497e-8888-515a05f02364 |
| Hybrid sleep | 238c9fa8-0aad-41ed-83f4-97be242c8f20 | 94ac6d29-73ce-41a6-809f-6363ba21b47e |
| WiFi Power Saving | 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 | 12bbebe6-58d6-4636-95bb-3217ef867c1a |
| PCIe ASPM | 501a4d13-42af-4429-9fd1-a8218c268e20 | ee12f906-d277-404b-b6da-e5fa1a576df5 |
| USB Selective Suspend | 2a737441-1930-4402-8d77-b2bebba308a3 | 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 |
| Wake Timers | 238c9fa8-0aad-41ed-83f4-97be242c8f20 | bd3b718a-0680-4d9d-8ab2-e1d2b4ac806d |