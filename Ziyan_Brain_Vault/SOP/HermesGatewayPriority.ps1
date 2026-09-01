<# 
.SYNOPSIS
    Hermes Gateway Process Priority & Power Throttling Fix
.DESCRIPTION
    Sets Hermes gateway processes (node.exe, python.exe) to High priority
    and disables power throttling for them. Run after gateway starts.
    Can be scheduled via Task Scheduler to run every 5 minutes.
#>

param(
    [switch]$InstallTask,
    [switch]$RemoveTask,
    [switch]$RunOnce
)

function Set-HermesProcessPriority {
    $processes = Get-Process -Name "node", "python" -ErrorAction SilentlyContinue
    if (-not $processes) {
        Write-Host "No Hermes gateway processes (node/python) found running." -ForegroundColor Yellow
        return
    }

    foreach ($p in $processes) {
        try {
            # Set to High priority (AboveNormal = 32768, High = 32768 in .NET, but we use enum)
            if ($p.PriorityClass -ne 'High') {
                $p.PriorityClass = 'High'
                Write-Host "Set $($p.ProcessName) (PID: $($p.Id)) priority to High" -ForegroundColor Green
            }

            # Disable Power Throttling (EcoQoS) for this process
            # Requires Windows 10 2004+ / Windows 11
            $result = powercfg /setprocesspowerthrottling $p.Id 0 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Disabled power throttling for $($p.ProcessName) (PID: $($p.Id))" -ForegroundColor Green
            } else {
                Write-Host "Power throttling control not available (older Windows version)" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "Failed to modify $($p.ProcessName) (PID: $($p.Id)): $_" -ForegroundColor Red
        }
    }
}

function Install-ScheduledTask {
    $action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -File "C:\Users\arija\HermesGatewayPriority.ps1" -RunOnce'
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration ([TimeSpan]::MaxValue)
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

    Register-ScheduledTask -TaskName "HermesGatewayPriority" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force
    Write-Host "Scheduled task 'HermesGatewayPriority' installed (runs every 5 min as SYSTEM)" -ForegroundColor Green
}

function Remove-ScheduledTask {
    Unregister-ScheduledTask -TaskName "HermesGatewayPriority" -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Scheduled task 'HermesGatewayPriority' removed" -ForegroundColor Green
}

if ($InstallTask) { Install-ScheduledTask }
elseif ($RemoveTask) { Remove-ScheduledTask }
else { Set-HermesProcessPriority }