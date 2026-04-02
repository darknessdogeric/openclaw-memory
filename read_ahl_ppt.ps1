# Read AHL PPT Content
Add-Type -AssemblyName Microsoft.Office.Interop.PowerPoint
$pp = New-Object -ComObject PowerPoint.Application
$pp.Visible = $false

# Find AHL business plan file
$desktopPath = [Environment]::GetFolderPath('Desktop')
$ahlFiles = Get-ChildItem "$desktopPath\AHL*.pptx"
$targetFile = $ahlFiles | Where-Object { $_.Name -like '*V6.0*' } | Select-Object -First 1

if ($targetFile) {
    Write-Host "Reading: $($targetFile.FullName)"
    $presentation = $pp.Presentations.Open($targetFile.FullName, $false, $false, $false)
    
    $slideCount = 0
    foreach ($slide in $presentation.Slides) {
        $slideCount++
        $title = ""
        $content = ""
        
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTitle) {
                $title = $shape.Title.TextFrame.TextRange.Text
            }
            if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
                $content = $shape.TextFrame.TextRange.Text
            }
        }
        
        if ($title -or $content) {
            Write-Host "--- Slide $slideCount ---"
            if ($title) { Write-Host "TITLE: $title" }
            if ($content) { Write-Host "CONTENT: $($content.Substring(0, [Math]::Min(200, $content.Length)))..." }
        }
        
        if ($slideCount -ge 25) { break }
    }
    
    $presentation.Close()
} else {
    Write-Host "No AHL V6.0 file found"
}

$pp.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($pp) | Out-Null