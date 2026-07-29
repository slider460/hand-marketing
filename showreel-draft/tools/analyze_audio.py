#!/usr/bin/env python3
# Анализ трека шоурила: BPM, сетка битов, энергия по секундам
import wave, json, os
import numpy as np

SCRATCH = os.path.dirname(os.path.abspath(__file__))
w = wave.open(os.path.join(SCRATCH, "audio/showreel.wav"), "rb")
sr = w.getframerate()
data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
w.close()

# --- onset envelope: спектральный поток ---
hop, win = 512, 1024
n = (len(data) - win) // hop
frames = np.lib.stride_tricks.as_strided(
    data, shape=(n, win), strides=(data.strides[0] * hop, data.strides[0]))
mag = np.abs(np.fft.rfft(frames * np.hanning(win), axis=1))
flux = np.maximum(mag[1:] - mag[:-1], 0).sum(axis=1)
flux = flux / (flux.max() + 1e-9)
fps = sr / hop  # ~43 fps огибающей

# --- BPM через автокорреляцию onset-огибающей ---
f = flux - flux.mean()
ac = np.correlate(f, f, mode="full")[len(f)-1:]
ac /= (ac[0] + 1e-9)
best_bpm, best_v = 0, -1
for bpm10 in range(600, 1900):  # 60..190 BPM с шагом 0.1
    bpm = bpm10 / 10
    lag = int(round(fps * 60 / bpm))
    if lag >= len(ac): continue
    v = ac[lag] + 0.5 * ac[min(2*lag, len(ac)-1)]
    if v > best_v:
        best_v, best_bpm = v, bpm
print("BPM:", best_bpm)

# --- фаза битов: максимум суммы onset по сетке ---
period = fps * 60 / best_bpm
best_ph, best_s = 0, -1
for ph in range(int(period)):
    idx = np.arange(ph, len(flux), period).astype(int)
    s = flux[idx].sum() / len(idx)
    if s > best_s:
        best_s, best_ph = s, ph
beats = np.arange(best_ph, len(flux), period) / fps
print("beats:", len(beats), "first:", np.round(beats[:8], 3).tolist())

# --- RMS-энергия по 0.5 c: структура трека ---
half = int(sr * 0.5)
nseg = len(data) // half
rms = [float(np.sqrt((data[i*half:(i+1)*half]**2).mean())) for i in range(nseg)]
rms = np.array(rms); rms /= rms.max()
print("Энергия по 2-сек блокам (0-9):")
for t in range(0, nseg - 3, 4):
    block = rms[t:t+4].mean()
    print(f"{t*0.5:6.1f}s {'#' * int(block*40)} {block:.2f}")

json.dump({"bpm": best_bpm, "beats": beats.tolist(), "rms_half_sec": rms.tolist()},
          open(os.path.join(SCRATCH, "audio/analysis.json"), "w"))
print("saved analysis.json")
