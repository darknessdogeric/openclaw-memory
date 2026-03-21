$extPath = "C:\Users\ericz\AppData\Local\Temp\opencli-extension\dist"
$chromePath = "C:\Users\ericz\AppData\Local\Google\Chrome\Application\chrome.exe"

Start-Process $chromePath -ArgumentList "--load-extension=$extPath","--no-first-run","--no-default-browser-check" -WindowStyle Normal
Write-Host "Chrome launched with extension"
