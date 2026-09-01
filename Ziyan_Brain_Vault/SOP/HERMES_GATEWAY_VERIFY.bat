@echo off
REM Verify Hermes Gateway 24/7 Fix Status
echo ============================================
echo HERMES GATEWAY FIX VERIFICATION
echo ============================================
echo.

echo [1] Modern Standby Mode:
powercfg /a | findstr /i "Network"

echo.
echo [2] EnforceDisconnectedStandby Registry:
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v EnforceDisconnectedStandby

echo.
echo [3] CsEnabled Registry:
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v CsEnabled

echo.
echo [4] WiFi Power Saving Mode (AC):
powercfg /query scheme_current SUB_SLEEP 12bbebe6-58d6-4636-95bb-3217ef867c1a | findstr /i "Current AC"

echo.
echo [5] WiFi Power Saving Mode (DC):
powercfg /query scheme_current SUB_SLEEP 12bbebe6-58d6-4636-95bb-3217ef867c1a | findstr /i "Current DC"

echo.
echo [6] PCI Express ASPM (AC/DC):
powercfg /query scheme_current SUB_PCIEXPRESS ASPM | findstr /i "Current"

echo.
echo [7] USB Selective Suspend (AC/DC):
powercfg /query scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 | findstr /i "Current"

echo.
echo [8] Hermes Gateway Processes Priority:
powershell -Command "Get-Process -Name node,python -ErrorAction SilentlyContinue | Select-Object Name, Id, PriorityClass | Format-Table -AutoSize"

echo.
echo ============================================
echo EXPECTED VALUES AFTER FIX:
echo - EnforceDisconnectedStandby = 0
echo - CsEnabled = 1  
echo - WiFi Power Saving = 0 (Maximum Performance) for both AC/DC
echo - PCI Express ASPM = 0 (Off) for both AC/DC
echo - USB Selective Suspend = 0 (Disabled) for both AC/DC
echo - Process Priority = High (or at least Normal)
echo ============================================
pause