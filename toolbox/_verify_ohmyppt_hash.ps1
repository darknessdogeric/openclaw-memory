$file = Get-Item 'C:\Users\ericz\Downloads\oh-my-ppt-2.1.0-win.exe'
$hash = (Get-FileHash -Path $file.FullName -Algorithm SHA256).Hash
Write-Output ('Size: ' + $file.Length + ' bytes (' + [math]::Round($file.Length/1MB, 2) + ' MB)')
Write-Output ('SHA256: ' + $hash)
Write-Output ('Expected: 96e18afea54c477f1baf4f7965dcc9102b5fcf641fb0758fdff72a4b624f92c9')
Write-Output ''
if ($hash -eq '96e18afea54c477f1baf4f7965dcc9102b5fcf641fb0758fdff72a4b624f92c9') {
    Write-Output 'HASH MATCH - installer authentic'
} else {
    Write-Output 'HASH MISMATCH - DO NOT INSTALL'
}