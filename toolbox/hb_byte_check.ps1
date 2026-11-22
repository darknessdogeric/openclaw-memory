# Check raw bytes around "AnYi" in HB #2192 entry
$f = 'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
$bytes = [System.IO.File]::ReadAllBytes($f)
$content = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)

# Find "AnYi 鎶ュ埌" location
$idx = $content.IndexOf('AnYi 鎶')
Write-Host 'AnYi mojibake at index:' $idx
if ($idx -gt 0) {
    $sub = $content.Substring($idx, 20)
    Write-Host 'Text (UTF-8 decoded):' $sub
    Write-Host 'Bytes around it:'
    $startByte = 0
    for ($i = 0; $i -lt $idx; $i++) {
        $startByte += [System.Text.Encoding]::UTF8.GetByteCount($content[$i].ToString())
    }
    Write-Host ('Byte position:' + $startByte)
    $byteSlice = $bytes[$startByte..($startByte + 30)]
    Write-Host ('Hex bytes: ' + [BitConverter]::ToString($byteSlice))
}

# Compare: what bytes would "AnYi 报到" produce?
$expected = 'AnYi 报到'
$expBytes = [System.Text.Encoding]::UTF8.GetBytes($expected)
Write-Host '---'
Write-Host ('Expected "AnYi 报到" UTF-8 bytes: ' + [BitConverter]::ToString($expBytes))

# What about reading "鎶ュ埌" as GB2312?
$mojibakeBytes = [System.Text.Encoding]::UTF8.GetBytes('鎶ュ埌')
Write-Host ('Mojibake "鎶ュ埌" UTF-8 bytes: ' + [BitConverter]::ToString($mojibakeBytes))
try {
    $decoded = [System.Text.Encoding]::GetEncoding('GB2312').GetString($mojibakeBytes)
    Write-Host ('GB2312 decode of mojibake bytes: ' + $decoded)
} catch {
    Write-Host 'GB2312 not available'
}
$decoded2 = [System.Text.Encoding]::GetEncoding(936).GetString($mojibakeBytes)
Write-Host ('CP936 decode of mojibake bytes: ' + $decoded2)