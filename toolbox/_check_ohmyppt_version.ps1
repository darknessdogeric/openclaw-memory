$vi = (Get-Item 'C:\Users\ericz\AppData\Local\Programs\ohmyppt\Uninstall ohmyppt.exe').VersionInfo
Write-Output "ProductVersion: $($vi.ProductVersion)"
Write-Output "FileVersion: $($vi.FileVersion)"
Write-Output "CompanyName: $($vi.CompanyName)"
Write-Output "FileDescription: $($vi.FileDescription)"
Write-Output ""
$exe = (Get-Item 'C:\Users\ericz\AppData\Local\Programs\ohmyppt\ohmyppt.exe').VersionInfo
Write-Output "--- ohmyppt.exe ---"
Write-Output "ProductVersion: $($exe.ProductVersion)"
Write-Output "FileVersion: $($exe.FileVersion)"
Write-Output "Comments: $($exe.Comments)"