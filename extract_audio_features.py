"""
Audio Feature Extraction Script - v2
Extract mathematical features: tempo, melody, key, harmony, etc.
"""

import os
import json
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
            if len(chroma_mean) > 0:
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

def analyze_playlist(folder_path, max_files=100, output_path="audio_features.json"):
    """Analyze audio files in folder"""
    folder = Path(folder_path)
    mp3_files = list(folder.glob("*.mp3")) + list(folder.glob("*.m4a"))
    
    results = {
        "folder": str(folder),
        "total_found": len(mp3_files),
        "analyzed": 0,
        "features": {}
    }
    
    print(f"Found {len(mp3_files)} audio files. Analyzing first {max_files}...")
    
    for i, audio_file in enumerate(mp3_files[:max_files]):
        try:
            print(f"[{i+1}/{max_files}] {audio_file.name[:50]}")
        except:
            print(f"[{i+1}/{max_files}] [unicode filename]")
        
        feats = extract_features(str(audio_file))
        if "error" not in feats:
            key = audio_file.stem[:80]
            results["features"][key] = feats
            results["analyzed"] += 1
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Analyzed: {results['analyzed']} songs")
    print(f"Results: {output_path}")
    
    # Summary statistics
    if results["analyzed"] > 0:
        tempos = [f["tempo_bpm"] for f in results["features"].values() if "tempo_bpm" in f]
        keys_count = {}
        energies = []
        brightness_values = []
        
        for f in results["features"].values():
            if "estimated_key" in f:
                k = f["estimated_key"]
                keys_count[k] = keys_count.get(k, 0) + 1
            if "energy_avg" in f:
                energies.append(f["energy_avg"])
            if "brightness_avg" in f:
                brightness_values.append(f["brightness_avg"])
        
        print(f"\n=== SUMMARY STATISTICS ===")
        print(f"Avg BPM: {np.mean(tempos):.1f}")
        print(f"BPM Range: {np.min(tempos):.1f} - {np.max(tempos):.1f}")
        print(f"Avg Energy: {np.mean(energies):.4f}")
        print(f"Avg Brightness (Hz): {np.mean(brightness_values):.0f}")
        
        # Top 5 keys
        sorted_keys = sorted(keys_count.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"Top Keys: {dict(sorted_keys)}")
        
        # Categorize by tempo
        slow = sum(1 for t in tempos if t < 80)
        medium = sum(1 for t in tempos if 80 <= t < 120)
        fast = sum(1 for t in tempos if t >= 120)
        print(f"Tempo Distribution: Slow(<80)={slow}, Medium(80-120)={medium}, Fast(>120)={fast}")
        
        # Categorize by brightness (warm vs bright)
        warm = sum(1 for b in brightness_values if b < 2000)
        medium_bright = sum(1 for b in brightness_values if 2000 <= b < 4000)
        very_bright = sum(1 for b in brightness_values if b >= 4000)
        print(f"Brightness Distribution: Warm(<2kHz)={warm}, Medium(2-4kHz)={medium_bright}, Bright(>4kHz)={very_bright}")
    
    return results

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else r"D:\CloudMusic\纷繁扰攘"
    output = r"C:\Users\ericz\.openclaw\workspace\audio_features.json"
    analyze_playlist(folder, max_files=200, output_path=output)
