# Discarded: failed to represent clear spectral bands with smooth transition

import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

# =============================
# 参数（以后主要改这里）
# =============================
AUDIO_DIR = r"/archive/songs/songs"
N_FILES = 2              # 现在画前 2 个，之后改成 len(files)
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512
DB_THRESHOLD = -25       # 你定义的“鸟叫阈值”

# =============================
# 读取 flac 文件
# =============================
files = sorted([f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".flac")])
files = files[:N_FILES]

# =============================
# 开始画图
# =============================
for idx, fname in enumerate(files):
    file_path = os.path.join(AUDIO_DIR, fname)

    y, sr = librosa.load(file_path, sr=SR)

    # STFT → 幅度 → dB
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    # 时间 & 频率坐标
    times = librosa.frames_to_time(np.arange(S_db.shape[1]), sr=sr, hop_length=HOP_LENGTH)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)

    # 展平成点云
    T, F = np.meshgrid(times, freqs)
    T = T.flatten()
    F = F.flatten()
    DB = S_db.flatten()

    # =============================
    # 只保留“鸟叫”（你现在的定义）
    # =============================
    mask = DB > DB_THRESHOLD
    T_bird = T[mask]
    F_bird = F[mask]

    # =============================
    # 画 frequency–time 密度图
    # =============================
    plt.figure(figsize=(10, 6))

    plt.hist2d(
        T_bird,
        F_bird,
        bins=[200, 200],
        cmap="YlOrBr"   # 橘黄色系
    )

    plt.colorbar(label="Density")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(f"Bird-call frequency bands (dB > {DB_THRESHOLD})\n{fname}")

    plt.tight_layout()
    plt.show()