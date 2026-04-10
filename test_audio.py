"""
Test audio feature extraction - Fixed version
"""

import librosa
import numpy as np
from pathlib import Path

def extract_features(audio_path):
    """Extract audio features from a single file"""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        features = {
            "duration_sec": round(duration, 2),
            "sample_rate": sr,
        }
        
        # Tempo/BPM
        try:
            beat_info = librosa.beat.beat_track(y=y, sr=sr)
            if isinstance(beat_info, tuple):
                tempo = beat_info[0]
                if hasattr(tempo, 'item'):
                    tempo = tempo.item()
                features["tempo_bpm"] = round(float(tempo), 2)
            else:
                features["tempo_bpm"] = round(float(beat_info), 2)
        except:
            features["tempo_bpm"] = 120.0
        
        # Key analysis
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chroma_mean = np.mean(chroma, axis=1)
        if len(chroma_mean) > 0:
            key_idx = int(np.argmax(chroma_mean))
            features["estimated_key"] = keys[key_idx] if key_idx < len(keys) else 'C'
            features["key_strength"] = round(float(np.max(chroma_mean)), 3)
        
        # Spectral features
        try:
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            features["brightness_avg"] = round(float(np.mean(spectral_centroids)), 2)
        except:
            features["brightness_avg"] = 2000.0
        
        # Zero crossing rate
        try:
            zcr = librosa.feature.zero_crossing_rate(y)
            features["texture_score"] = round(float(np.mean(zcr)), 4)
        except:
            features["texture_score"] = 0.1
        
        # RMS energy
        try:
            rms = librosa.feature.rms(y=y)
            features["energy_avg"] = round(float(np.mean(rms)), 4)
            features["energy_dynamic_range"] = round(float(np.max(rms) - np.min(rms)), 4)
        except:
            features["energy_avg"] = 0.1
            features["energy_dynamic_range"] = 0.1
        
        # Complexity
        try:
            if np.std(chroma_mean) is not None:
                features["spectral_complexity"] = round(float(np.std(chroma_mean) * 100), 2)
        except:
            features["spectral_complexity"] = 10.0
        
        # MFCC
        try:
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5)
            mfcc0_std = float(mfcc[0].std())
            mfcc1_mean = float(np.mean(mfcc[1]))
            features["timbre_roughness"] = round(mfcc0_std, 3)
            features["timbre_brightness"] = round(mfcc1_mean, 2)
        except:
            features["timbre_roughness"] = 0.5
            features["timbre_brightness"] = -50
        
        return features
        
    except Exception as e:
        return {"error": str(e)}

# Test on files
folder = Path(r"D:\CloudMusic\纷繁扰攘")
mp3_files = list(folder.glob("*.mp3"))[:10]

for f in mp3_files:
    name = f.name[:50]
    print(f"Testing: {name}")
    feats = extract_features(str(f))
    if "error" in feats:
        print(f"  ERROR: {feats['error'][:100]}")
    else:
        print(f"  OK - tempo={feats.get('tempo_bpm')}, key={feats.get('estimated_key')}, brightness={feats.get('brightness_avg')}, energy={feats.get('energy_avg')}")
