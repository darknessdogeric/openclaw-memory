# 网易云音乐 - 批量获取歌曲详情
# 功能：根据track IDs批量获取歌曲详细信息

import subprocess
import json
import time
import sys

# 纷繁扰攘歌单的track IDs（从API获取到的部分ID）
# 由于API限制，这里用已知的大数量track ID来测试
# 实际应该从歌单API获取完整trackIds列表

def get_playlist_track_ids(playlist_id):
    """获取歌单的所有track IDs"""
    url = f'https://music.163.com/api/v6/playlist/detail?id={playlist_id}&n=10000'
    cmd = ['curl', '-s', url, '-H', 'User-Agent: Mozilla/5.0', '-H', 'Referer: https://music.163.com/']
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    if data.get('code') != 200:
        print(f"API错误: {data}")
        return []
    
    track_ids = []
    for item in data.get('result', {}).get('trackIds', []):
        track_ids.append(item['id'])
    
    print(f"获取到 {len(track_ids)} 个track IDs")
    return track_ids

def get_song_details(track_ids, batch_size=100):
    """批量获取歌曲详情"""
    all_songs = []
    total = len(track_ids)
    
    for i in range(0, total, batch_size):
        batch = track_ids[i:i+batch_size]
        ids_param = ','.join(map(str, batch))
        url = f'https://music.163.com/api/v3/song/detail?ids=[{ids_param}]'
        
        cmd = ['curl', '-s', url, '-H', 'User-Agent: Mozilla/5.0', '-H', 'Referer: https://music.163.com/']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        try:
            data = json.loads(result.stdout)
            songs = data.get('songs', [])
            all_songs.extend(songs)
            print(f"批次 {i//batch_size + 1}: 获取 {len(songs)} 首 (总计 {len(all_songs)}/{total})")
        except json.JSONDecodeError:
            print(f"批次 {i//batch_size + 1} JSON解析失败")
        
        if i + batch_size < total:
            time.sleep(0.3)  # 避免请求过快
    
    return all_songs

def analyze_songs(songs):
    """分析歌曲数据"""
    print(f"\n{'='*60}")
    print(f"分析结果：共 {len(songs)} 首歌曲")
    print(f"{'='*60}")
    
    # 按语言/地区分类
    regions = {'中文': 0, '日语': 0, '英语': 0, '俄语/西里尔': 0, '其他': 0}
    decades = {'60s及以前': 0, '70s': 0, '80s': 0, '90s': 0, '2000s': 0, '2010s': 0, '2020s': 0, '未知': 0}
    artists = {}
    albums = {}
    
    for song in songs:
        # 艺术家
        if song.get('ar'):
            for artist in song['ar']:
                name = artist.get('name', 'Unknown')
                artists[name] = artists.get(name, 0) + 1
        
        # 专辑
        if song.get('al'):
            album_name = song['al'].get('name', 'Unknown')
            albums[album_name] = albums.get(album_name, 0) + 1
        
        # 尝试识别语言（通过艺术家名或歌曲名中的字符）
        artist_name = song.get('ar', [{}])[0].get('name', '') if song.get('ar') else ''
        song_name = song.get('name', '')
        
        # 简单语言检测
        has_cjk = any('\u4e00' <= c <= '\u9fff' for c in artist_name + song_name)
        has_japanese = any('\u3040' <= c <= '\u30ff' for c in artist_name + song_name)
        has_cyrillic = any('\u0400' <= c <= '\u04ff' for c in artist_name + song_name)
        
        if has_japanese:
            regions['日语'] += 1
        elif has_cyrillic:
            regions['俄语/西里尔'] += 1
        elif has_cjk:
            regions['中文'] += 1
        else:
            regions['英语'] += 1
        
        # 年份（从发布年份推断）
        publish_time = song.get('al', {}).get('publishTime', 0) if song.get('al') else 0
        if publish_time > 0:
            year = (publish_time // (365 * 24 * 60 * 60 * 1000)) + 1970
            if year < 1970:
                decades['60s及以前'] += 1
            elif year < 1980:
                decades['70s'] += 1
            elif year < 1990:
                decades['80s'] += 1
            elif year < 2000:
                decades['90s'] += 1
            elif year < 2010:
                decades['2000s'] += 1
            elif year < 2020:
                decades['2010s'] += 1
            else:
                decades['2020s'] += 1
        else:
            decades['未知'] += 1
    
    print("\n【按语言/地区】")
    for region, count in sorted(regions.items(), key=lambda x: -x[1]):
        pct = count / len(songs) * 100 if songs else 0
        print(f"  {region}: {count}首 ({pct:.1f}%)")
    
    print("\n【按年代】")
    for decade, count in decades.items():
        pct = count / len(songs) * 100 if songs else 0
        print(f"  {decade}: {count}首 ({pct:.1f}%)")
    
    print("\n【热门艺术家 TOP 15】")
    sorted_artists = sorted(artists.items(), key=lambda x: -x[1])[:15]
    for artist, count in sorted_artists:
        print(f"  {artist}: {count}首")
    
    print("\n【热门专辑 TOP 15】")
    sorted_albums = sorted(albums.items(), key=lambda x: -x[1])[:15]
    for album, count in sorted_albums:
        print(f"  {album}: {count}首")
    
    # 保存详细数据
    with open('fenran_songs_detail.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print(f"\n详细数据已保存到 fenran_songs_detail.json")
    
    # 保存分析摘要
    analysis = {
        'total_songs': len(songs),
        'by_region': regions,
        'by_decade': decades,
        'top_artists': dict(sorted(artists.items(), key=lambda x: -x[1])[:30]),
        'top_albums': dict(sorted(albums.items(), key=lambda x: -x[1])[:30])
    }
    with open('fenran_analysis_summary.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"分析摘要已保存到 fenran_analysis_summary.json")

def main():
    playlist_id = 422540795  # 纷繁扰攘
    
    print("步骤1: 获取歌单track IDs...")
    track_ids = get_playlist_track_ids(playlist_id)
    
    if not track_ids:
        print("无法获取track IDs，使用已知数据...")
        return
    
    print(f"\n步骤2: 批量获取 {len(track_ids)} 首歌曲详情...")
    songs = get_song_details(track_ids[:1000])  # 限制前1000首进行分析
    
    if songs:
        analyze_songs(songs)
    else:
        print("无法获取歌曲详情")

if __name__ == '__main__':
    main()
