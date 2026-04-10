"""Quick audio analysis - 10 songs only"""
import librosa
import numpy as np
from pathlib import Path
import json

folder = Path(r'D:\CloudMusic\纷繁扰攘')
mp3_files = list(folder.glob('*.mp3'))[:10]

results = {'songs': []}

for f in mp3_files:
    print('Analyzing:', f.name[:40])
    try:
        y, sr = librosa.load(str(f), sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Tempo
        beat_info = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(beat_info[0].item()) if hasattr(beat_info[0], 'item') else float(beat_info[0])
        
        # Key
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        key_idx = int(np.argmax(np.mean(chroma, axis=1)))
        key = keys[key_idx] if key_idx < len(keys) else 'C'
        
        # Brightness
        sc = librosa.feature.spectral_centroid(y=y, sr=sr)
        brightness = float(np.mean(sc))
        
        # Energy
        rms = librosa.feature.rms(y=y)
        energy = float(np.mean(rms))
        
        results['songs'].append({
            'name': f.name[:50],
            'duration': round(duration, 1),
            'tempo': round(tempo, 1),
            'key': key,
            'brightness': round(brightness, 0),
            'energy': round(energy, 4)
        })
        print(f'  -> tempo={round(tempo,1)}, key={key}, brightness={round(brightness,0)}Hz, energy={round(energy,4)}')
    except Exception as e:
        print('ERROR:', str(e)[:50])

# Summary
print('\n=== SUMMARY ===')
tempos = [s['tempo'] for s in results['songs']]
print('Avg BPM:', round(np.mean(tempos), 1))
print('Tempo range:', min(tempos), '-', max(tempos))
keys = [s['key'] for s in results['songs']]
from collections import Counter
print('Keys:', dict(Counter(keys)))
brightness = [s['brightness'] for s in results['songs']]
print('Avg brightness:', round(np.mean(brightness), 0), 'Hz')

# Save
with open(r'C:\Users\ericz\.openclaw\workspace\audio_features.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('\nSaved to audio_features.json')
