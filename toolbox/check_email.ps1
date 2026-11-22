try {
    $outlook = New-Object -ComObject Outlook.Application
    $namespace = $outlook.GetNamespace('MAPI')
    $inbox = $namespace.GetDefaultFolder(6)
    $items = $inbox.Items
    $items.Sort('[ReceivedTime]', $true)
    $recent = @()
    for ($i = 0; $i -lt [Math]::Min(5, $items.Count); $i++) {
        $m = $items[$i]
        if ($m.ReceivedTime -gt (Get-Date).AddHours(-24)) {
            $recent += [PSCustomObject]@{
                From = $m.SenderName
                Subject = $m.Subject
                Time = $m.ReceivedTime.ToString('MM-dd HH:mm')
                HasAttachments = $m.Attachments.Count
                Unread = $m.UnRead
            }
        }
    }
    if ($recent.Count -eq 0) { Write-Output 'NO_RECENT_EMAIL' }
    else { $recent | Format-Table -AutoSize | Out-String }
} catch {
    Write-Output "EMAIL_CHECK_FAILED: $_"
}
