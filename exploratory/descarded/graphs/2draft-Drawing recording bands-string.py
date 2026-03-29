# Discarded: timing was collapsed, leading to a loss of temporal precision. + used incorrect data.

import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# =============================
# 参数（你以后主要改这里）
# =============================
AUDIO_DIR = r"/archive/songs/songs"
ENERGY_THRESHOLD_DB = -25
N_FFT = 2048
HOP_LENGTH = 512
MAX_FILES = 2

# =============================
# 找 flac 文件
# =============================
flac_files = [
    os.path.join(AUDIO_DIR, f)
    for f in os.listdir(AUDIO_DIR)
    if f.lower().endswith(".flac")
][:MAX_FILES]

# =============================
# 主循环
# =============================
for idx, file_path in enumerate(flac_files, 1):
    y, sr = librosa.load(file_path, sr=None)

    # STFT → 幅度 → dB
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    freqs = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)
    times = librosa.frames_to_time(
        np.arange(S_db.shape[1]), sr=sr, hop_length=HOP_LENGTH
    )

    # =============================
    # 只保留高能量（≥ -25 dB）
    # =============================
    mask = S_db >= ENERGY_THRESHOLD_DB

    # 每个频率 bin：高能量出现的“次数”
    freq_density = mask.sum(axis=1)

    # 归一化，让它像“一条带子”
    freq_density = freq_density / freq_density.max()

    # =============================
    # 画图
    # =============================
    plt.figure(figsize=(6, 4))

    plt.imshow(
        freq_density[:, np.newaxis],
        origin="lower",
        aspect="auto",
        extent=[0, 1, freqs[0], freqs[-1]],
        cmap="YlOrBr"
    )

    plt.colorbar(label="Relative occurrence density")
    plt.xlabel("Time (collapsed)")
    plt.ylabel("Frequency (Hz)")
    plt.title(f"Frequency band (Energy ≥ {ENERGY_THRESHOLD_DB} dB)\nFile {idx}")

    plt.tight_layout()
    plt.show()