@echo off
REM HERMES GATEWAY 24/7 CONNECTIVITY FIX
REM Run as Administrator (Right-click -> Run as Administrator)

echo ============================================
echo HERMES GATEWAY 24/7 CONNECTIVITY FIX
echo ============================================
echo.

echo [1/6] Enabling Network Connectivity in Modern Standby (S0ix)...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v EnforceDisconnectedStandby /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v CsEnabled /t REG_DWORD /d 1 /f

echo.
echo [2/6] Setting WiFi Power Saving to Maximum Performance (AC + DC)...
powercfg /setacvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0
powercfg /setdcvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0

echo.
echo [3/6] Disabling USB Selective Suspend (AC + DC)...
powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

echo.
echo [4/6] Disabling PCI Express ASPM (AC + DC)...
powercfg /setacvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0
powercfg /setdcvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0

echo.
echo [5/6] Applying power plan changes...
powercfg /setactive scheme_current

echo.
echo [6/6] Verifying Modern Standby mode...
powercfg /a

echo.
echo ============================================
echo FIX APPLIED - REBOOT REQUIRED FOR REGISTRY CHANGES
echo ============================================
echo.
echo After reboot, verify with: powercfg /a
echo Should show: "Standby (S0 Low Power Idle) Network Connected" as available
echo.
pause