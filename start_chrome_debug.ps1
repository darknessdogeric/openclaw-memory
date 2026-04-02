# Kill all Chrome
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# Start Chrome with remote debugging
$exePath = "C:\Users\ericz\AppData\Local\Google\Chrome\Application\chrome.exe"
$userDataDir = "$env:LOCALAPPDATA\Google\Chrome\User Data\DebugProfile"
$port = 9222

# Ensure debug profile dir exists
if (-not (Test-Path $userDataDir)) {
    New-Item -ItemType Directory -Path $userDataDir -Force | Out-Null
}

$args = @(
    "--remote-debugging-port=$port",
    "--user-data-dir=`"$userDataDir`"",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--new-window"
)

$proc = Start-Process -FilePath $exePath -ArgumentList $args -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 5

if ($proc.HasExited) {
    Write-Host "Chrome exited with code: $($proc.ExitCode)"
} else {
    Write-Host "Chrome started with PID: $($proc.Id)"
}

# Verify port
$conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "SUCCESS: Debug port $port is listening!"
} else {
    Write-Host "WARNING: Port $port not listening yet"
}
