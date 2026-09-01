=== HERMES GATEWAY 24/7 CONNECTIVITY FIX ===
Root Cause Analysis:
====================

1. MODERN STANDBY (S0ix) - NETWORK DISCONNECTED MODE
   - powercfg /a shows: "Standby (S0 Low Power Idle) Network Disconnected" = ACTIVE
   - "Standby (S0 Low Power Idle) Network Connected" = "Connectivity in standby is not supported"
   - Registry: HKLM\SYSTEM\CurrentControlSet\Control\Power\EnforceDisconnectedStandby = 1
   - This FORCES network disconnection when screen turns off/locks

2. WIFI POWER SAVING MODE (Power Plan)
   - Wireless Adapter Settings > Power Saving Mode:
     * AC (plugged in): Maximum Performance (0) - GOOD
     * DC (battery): Medium Power Saving (2) - PROBLEMATIC

3. INTEL WIFI DRIVER SETTINGS (Already Optimal)
   - MIMOPowerSaveMode = 0 (Disabled) - GOOD
   - uAPSDSupport = 0 (WMM Power Save Off) - GOOD
   - WakeOnMagicPacket = 1, WakeOnPattern = 1 - GOOD
   - IbssTxPower = 100 (Max) - GOOD

4. PROCESS PRIORITY / THROTTLING
   - Python/Node processes run at "BelowNormal" priority
   - Windows throttles background processes further on lock screen

5. PCI EXPRESS ASPM - Already Off (0) on both AC/DC - GOOD
6. USB SELECTIVE SUSPEND - Already Disabled - GOOD
7. SLEEP AFTER - Already 0 (Never) on AC/DC - GOOD

=== EXACT FIX COMMANDS (Run as Administrator) ===

# 1. CRITICAL: Enable Network Connectivity in Modern Standby (S0ix)
# This is the MAIN FIX - changes "Network Disconnected" to "Network Connected"
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v EnforceDisconnectedStandby /t REG_DWORD /d 0 /f

# 2. Set WiFi Power Saving to Maximum Performance on BOTH AC and DC
powercfg /setacvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0
powercfg /setdcvalueindex scheme_current 19cbb8fa-5279-450e-9fac-8a3d5fedd0c1 12bbebe6-58d6-4636-95bb-3217ef867c1a 0
powercfg /setactive scheme_current

# 3. Disable Modern Standby Network Disconnect via CsEnabled (if exists)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v CsEnabled /t REG_DWORD /d 1 /f

# 4. Disable Power Throttling for Hermes Gateway Process
# Run this AFTER starting Hermes gateway to get the PID:
# powercfg /setprocesspowerthrottling <PID> 0

# 5. Set Hermes Gateway Process to High Priority (run after gateway starts)
# wmic process where "name='node.exe' or name='python.exe'" CALL setpriority 128
# OR in PowerShell:
# (Get-Process -Name node,python).PriorityClass = 'High'

# 6. Prevent USB selective suspend (already disabled but ensure)
powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

# 7. Disable PCI Express ASPM (already off but ensure)
powercfg /setacvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0
powercfg /setdcvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0

# 8. Apply all power plan changes
powercfg /setactive scheme_current

# 9. Verify Modern Standby now shows Network Connected
powercfg /a

=== AUTOMATION: Create a Scheduled Task to Keep Priority High ===

# Save as: C:\Scripts\HermesGatewayPriority.ps1
# $processes = Get-Process -Name node,python -ErrorAction SilentlyContinue
# foreach ($p in $processes) { if ($p.PriorityClass -ne 'High') { $p.PriorityClass = 'High' } }
# 
# Create Task Scheduler: Run every 5 min, highest privileges, trigger on workstation lock/unlock

=== VERIFICATION COMMANDS ===

# Check Modern Standby mode (should show "Network Connected" available)
powercfg /a

# Check EnforceDisconnectedStandby (should be 0)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Power" /v EnforceDisconnectedStandby

# Check WiFi Power Saving Mode (should be 0 for both AC/DC)
powercfg /query scheme_current SUB_SLEEP 12bbebe6-58d6-4636-95bb-3217ef867c1a

# Check process priority
Get-Process -Name node,python | Select-Object Name, Id, PriorityClass

=== NOTES ===
- Requires REBOOT after registry changes for Modern Standby to take effect
- The EnforceDisconnectedStandby=0 change allows Windows to maintain network in S0ix
- Some laptops may not support "Network Connected" Modern Standby due to firmware
- If Network Connected still shows "not supported", the hardware/firmware doesn't support it
- In that case, use "Presentation Mode" or a keep-awake tool as workaround