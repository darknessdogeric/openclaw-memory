import librosa
import numpy as np
from pathlib import Path
import json

def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        features = {'duration_sec': round(duration, 2), 'sample_rate': sr}
        try:
            beat_info = librosa.beat.beat_track(y=y, sr=sr)
            if isinstance(beat_info, tuple):
                tempo = beat_info[0]
                if hasattr(tempo, 'item'): tempo = tempo.item()
                features['tempo_bpm'] = round(float(tempo), 2)
            else:
                features['tempo_bpm'] = round(float(beat_info), 2)
        except: features['tempo_bpm'] = 120.0
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        chroma_mean = np.mean(chroma, axis=1)
        if len(chroma_mean) > 0:
            key_idx = int(np.argmax(chroma_mean))
            features['estimated_key'] = keys[key_idx] if key_idx < len(keys) else 'C'
        try:
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            features['brightness_avg'] = round(float(np.mean(spectral_centroids)), 2)
        except: features['brightness_avg'] = 2000.0
        try:
            zcr = librosa.feature.zero_crossing_rate(y)
            features['texture_score'] = round(float(np.mean(zcr)), 4)
        except: features['texture_score'] = 0.1
        try:
            rms = librosa.feature.rms(y=y)
            features['energy_avg'] = round(float(np.mean(rms)), 4)
        except: features['energy_avg'] = 0.1
        return features
    except Exception as e:
        return {'error': str(e)}

folder = Path(r'D:\CloudMusic\纷繁扰攘')
mp3_files = list(folder.glob('*.mp3'))[:50]
results = {'analyzed': 0, 'features': {}}
for i, f in enumerate(mp3_files):
    feats = extract_features(str(f))
    if 'error' not in feats:
        results['features'][f.stem[:50]] = feats
        results['analyzed'] += 1
    if (i+1) % 10 == 0:
        print('Progress:', i+1, '/50')
print('Done! Analyzed:', results['analyzed'])
tempos = [f['tempo_bpm'] for f in results['features'].values() if 'tempo_bpm' in f]
keys_count = {}
for f in results['features'].values():
    if 'estimated_key' in f:
        k = f['estimated_key']
        keys_count[k] = keys_count.get(k, 0) + 1
print('Avg BPM:', np.mean(tempos))
print('Top Keys:', dict(sorted(keys_count.items(), key=lambda x: x[1], reverse=True)[:5]))
with open(r'C:\Users\ericz\.openclaw\workspace\audio_features.json', 'w') as fp:
    json.dump(results, fp, ensure_ascii=False, indent=2)
