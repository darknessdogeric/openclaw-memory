# Stop OpenClaw gateway (waits up to 30s for graceful shutdown)
$gateway = Get-Process -Name "openclaw", "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*gateway*" -or $_.MainWindowTitle -like "*OpenClaw*" } | Select-Object -First 5
if ($gateway) {
    Write-Host "[1/4] Stopping gateway processes..." -ForegroundColor Yellow
    $gateway | ForEach-Object {
        Write-Host "  Stopping PID $($_.Id) ($($_.ProcessName))..."
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/4] No gateway processes found via process scan" -ForegroundColor Gray
}

# Official stop (preferred)
Write-Host "[1/4] Running openclaw daemon stop..." -ForegroundColor Yellow
& "C:\Users\ericz\.openclaw\tmp\agent-cli\openclaw.cmd" daemon stop 2>&1 | Out-String
Start-Sleep -Seconds 5

# Verify gateway is down
$stillRunning = Get-Process -Name "openclaw", "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*gateway*" }
if ($stillRunning) {
    Write-Host "[1/4] WARN: gateway still running. Force kill..." -ForegroundColor Red
    $stillRunning | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
}
Write-Host "[1/4] OK - gateway stopped" -ForegroundColor Green