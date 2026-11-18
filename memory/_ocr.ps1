$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime | Out-Null
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Foundation, ContentType=WindowsRuntime]

Add-Type -Path 'D:\B166ER-openclaw\workspace\tools\winrt_async.ps1' -ErrorAction SilentlyContinue

function Await($op, $type) {
  $task = [System.WindowsRuntimeSystemExtensions]::AsTask($op)
  $task.Wait(-1) | Out-Null
  $task.Result
}

$img = 'D:\B166ER-openclaw\workspace\media\inbound\openclaw-staged-ebdea283-4b35-4097-8dec-2a642a2a9045\input-image---1b1867e8-83f2-444a-9521-5d7babc81278.png'
$out = 'D:\B166ER-openclaw\workspace\output\award_form\ocr.txt'

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if (-not $engine) { Write-Output 'NO_ENGINE'; exit 1 }
Write-Output ('engine lang: ' + $engine.RecognizerLanguage.LanguageTag)

$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($img)) ([Windows.Storage.StorageFile])
$stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])

$all = New-Object System.Collections.Generic.List[string]

for ($band = 0; $band -lt 6; $band++) {
  $y0 = [int](1407 * 0 + 6300 / 6 * $band)
  $y1 = [int](6300 / 6 * ($band + 1) + 30)
  if ($y1 -gt 6300) { $y1 = 6300 }
  $bmp = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $crop = Await ($bmp.CropAsync((New-Object Windows.Graphics.Rectangle(0, $y0, 1407, ($y1 - $y0))))) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $res = Await ($engine.RecognizeAsync($crop)) ([Windows.Media.Ocr.OcrResult])
  $all.Add('===== BAND ' + $band + ' (y=' + $y0 + '..' + $y1 + ') =====')
  foreach ($line in $res.Lines) { $all.Add($line.Text) }
  Write-Output ('band ' + $band + ' lines: ' + $res.Lines.Count)
}

$all -join [Environment]::NewLine | Set-Content -Path $out -Encoding UTF8
Write-Output ('OCR written: ' + (Get-Item $out).Length + ' B')