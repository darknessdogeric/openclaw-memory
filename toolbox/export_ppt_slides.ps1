$src = 'C:\Users\ericz\Desktop\产业发展部人事\培训资料\【Edit】PPT_ 酒店行业速查表 · 核心概念.pptx'
$ole = New-Object -ComObject PowerPoint.Application
$pres = $ole.Presentations.Open($src)
$pres.Slides.Item(1).Export('D:\B166ER-OpenClaw\workspace\85review_v2\ppt_slide1.png', 'PNG', 1920, 1080)
$pres.Slides.Item(2).Export('D:\B166ER-OpenClaw\workspace\85review_v2\ppt_slide2.png', 'PNG', 1920, 1080)
$pres.Close()
$ole.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($ole)
Write-Host 'OK'