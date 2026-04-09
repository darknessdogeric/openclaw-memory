# 网易云音乐歌单抓取脚本
# 功能：分批获取歌单中的所有歌曲，保存为JSON

param(
    [int]$PlaylistId = 422540795,
    [string]$OutputFile = "fenran_tracks.json",
    [int]$BatchSize = 500
)

$ErrorActionPreference = "Continue"

$baseUrl = "https://music.163.com/api/playlist/detail?id=$PlaylistId"
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "Referer" = "https://music.163.com/"
}

Write-Host "开始获取歌单 $PlaylistId 的歌曲列表..."

# 获取第一页获取总数
try {
    $response = Invoke-RestMethod -Uri $baseUrl -Headers $headers -TimeoutSec 30
    $playlist = $response.result
    
    $total = $playlist.trackCount
    $name = $playlist.name
    
    Write-Host "歌单名称: $name"
    Write-Host "总歌曲数: $total"
    Write-Host "API返回的首批歌曲数: $($playlist.tracks.Count)"
    
    # 收集所有歌曲
    $allTracks = @()
    
    # 先添加已经返回的tracks
    foreach ($track in $playlist.tracks) {
        $allTracks += $track
    }
    
    Write-Host "已收集: $($allTracks.Count) 首"
    
    # 如果总数超过返回的数量，需要用其他方式获取
    # 网易云的API对于大歌单可能只返回部分
    # 尝试通过获取所有track IDs再逐个获取详情
    
    if ($total -gt $allTracks.Count) {
        Write-Host "歌单较大，尝试通过track id列表获取完整数据..."
        
        # 获取歌单的track ids
        $trackIdsUrl = "https://music.163.com/api/playlist/track/detail?id=$PlaylistId"
        
        # 分批获取，每批1000首
        $idsPerBatch = 1000
        $offset = 0
        
        while ($offset -lt $total) {
            $batchIdsUrl = "https://music.163.com/api/playlist/track/list?id=$PlaylistId&idx=$offset&cnt=$idsPerBatch"
            
            try {
                $idsResponse = Invoke-RestMethod -Uri $batchIdsUrl -Headers $headers -TimeoutSec 30
                
                if ($idsResponse.code -eq 200 -and $idsResponse.songs) {
                    $batchCount = $idsResponse.songs.Count
                    Write-Host "  获取批次 $offset - $offset+$batchCount"
                    
                    foreach ($song in $idsResponse.songs) {
                        $allTracks += $song
                    }
                    
                    if ($batchCount -lt $idsPerBatch) {
                        break
                    }
                } else {
                    break
                }
            }
            catch {
                Write-Host "  批次获取失败: $_"
                break
            }
            
            $offset += $idsPerBatch
        }
    }
    
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "最终收集到的歌曲总数: $($allTracks.Count)"
    Write-Host "=========================================="
    
    # 保存到文件
    $allTracks | ConvertTo-Json -Depth 20 | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Host "已保存到: $OutputFile"
    
    # 输出统计
    Write-Host ""
    Write-Host "========= 初步统计分析 ========="
    
    # 按语言/地区分类统计
    $artistRegions = @{}
    $albumYears = @{}
    $popularityStats = @{}
    
    foreach ($track in $allTracks) {
        # 提取艺术家名
        $artistName = "Unknown"
        if ($track.artists -and $track.artists.Count -gt 0) {
            $artistName = $track.artists[0].name
        }
        
        # 检测语言/地区
        $region = "Other"
        if ($artistName -match "[\u4e00-\u9fff]") {
            $region = "Chinese"
        } elseif ($artistName -match "[\u3040-\u309f\u30a0-\u30ff]") {
            $region = "Japanese"
        } elseif ($artistName -match "[\u0400-\u04ff]") {
            $region = "Russian/Сyrillic"
        }
        
        $artistRegions[$region] = ($artistRegions[$region] + 1)
        
        # 年份统计
        if ($track.album) {
            $year = "Unknown"
            if ($track.album.publishTime -and $track.album.publishTime -gt 0) {
                $year = (Get-Date $track.album.publishTime -Format "yyyy")
            }
            $albumYears[$year] = ($albumYears[$year] + 1)
        }
        
        # 热度统计
        $pop = "Low"
        if ($track.popularity -ge 80) { $pop = "High" }
        elseif ($track.popularity -ge 50) { $pop = "Medium" }
        $popularityStats[$pop] = ($popularityStats[$pop] + 1)
    }
    
    Write-Host ""
    Write-Host "【按语言/地区】"
    $artistRegions.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object {
        Write-Host "  $($_.Key): $($_.Value) 首"
    }
    
    Write-Host ""
    Write-Host "【按发行年份】"
    $albumYears.GetEnumerator() | Sort-Object Name | ForEach-Object {
        Write-Host "  $($_.Key): $($_.Value) 首"
    }
    
    Write-Host ""
    Write-Host "【按热度】"
    $popularityStats.GetEnumerator() | ForEach-Object {
        Write-Host "  $($_.Key): $($_.Value) 首"
    }
    
    # 保存详细分析
    $analysis = @{
        total = $allTracks.Count
        byRegion = $artistRegions
        byYear = $albumYears
        byPopularity = $popularityStats
    }
    
    $analysis | ConvertTo-Json -Depth 10 | Out-File -FilePath "fenran_analysis.json" -Encoding UTF8
    
}
catch {
    Write-Host "错误: $_"
}
