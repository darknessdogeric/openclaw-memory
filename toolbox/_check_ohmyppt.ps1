$shell = New-Object -ComObject WScript.Shell
$lnk = $shell.CreateShortcut('C:\Users\ericz\Desktop\OhMyPPT.lnk')
Write-Output 'TargetPath:'
Write-Output $lnk.TargetPath
Write-Output 'Arguments:'
Write-Output $lnk.Arguments
Write-Output 'WorkingDirectory:'
Write-Output $lnk.WorkingDirectory
Write-Output 'IconLocation:'
Write-Output $lnk.IconLocation