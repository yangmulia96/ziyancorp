@echo off
:: Jalankan sebagai Administrator (right-click -> Run as Admin)
:: Matikan Dell bloatware + Office telemetry dari SERVICE, STARTUP, DAN SCHEDULER
:: Tujuan: cuma Hermes + 9router + cua-driver + Hermes_Gateway yang auto-jalan.
echo ======================== ZIYAN CLEANUP ========================
echo [1/3] Disable Dell/Office SERVICES...
for %%S in (DDVService DDVCollector DDVProcessor DellSupportAssistRemediation DellDigitalDeliveryServices DellHardwareSupport "Dell Command Power Manager Notify" DellMgmtStudio WaveSvc WavesAudioService SmartByte SmartByteTelemetry DellMobileConnectService) do (
  sc config "%%S" start= disabled >nul 2>&1
  sc stop "%%S" >nul 2>&1
  echo   - %%S disabled
)
echo [2/3] Disable STARTUP entries (registry)...
for %%R in ("WavesSvc" "DellMobileConnectWelcome" "SPDriverInstall" "IAStorIcon" "GoogleChromeAutoLaunch_27236686920DADBA8938676EEE1E7BD6") do (
  reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "%%R" /f >nul 2>&1
  echo   - startup %%R removed
)
echo [3/3] Disable SCHEDULER tasks (Office + SmartByte)...
for %%T in ("SmartByte Telemetry" "Office Actions Server" "Office Automatic Updates 2.0" "Office Background Push Maintenance" "Office Feature Updates Logon" "Office Startup Maintenance") do (
  schtasks /Change /TN "%%T" /DISABLE >nul 2>&1
  echo   - task %%T disabled
)
echo ======================== SELESAI ========================
echo Yang TETAP auto-jalan: Hermes, 9router, cua-driver, Hermes_Gateway, Defender, OneDrive, Realtek.
echo Restart laptop untuk efek penuh.
pause
