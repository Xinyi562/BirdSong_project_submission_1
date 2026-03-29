# This code is discarded since it includes unnecessary loops
import os
import random
import numpy as np
#import librosa
import librosa.display
import matplotlib.pyplot as plt
from utils.find_project_root import find_project_root



# Finding the relative path for AUDIO_DIR.
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = find_project_root(__file__)
AUDIO_DIR = os.path.join(BASE_DIR, "archive", "songs")

SR = 22050
N_FFT = 2048
HOP_LENGTH = 512
idx = 48  # 前10个 or 随机10个

# =============================
# 选音频文件
# =============================
audio_files = [
    os.path.join(AUDIO_DIR, f)
    for f in os.listdir(AUDIO_DIR)
    if f.lower().endswith((".wav", ".flac", ".mp3"))
]

selected_files = audio_files[idx:idx + 1]
#selected_files = random.sample(audio_files, idx)

# =============================
# 画图
# =============================
plt.figure(figsize=(12, 6))

for i, filepath in enumerate(selected_files, 1):
    y, sr = librosa.load(filepath, sr=SR)

    # STFT
    S = np.abs(librosa.stft(
        y,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH
    ))

    # 转 dB
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    # 👉 每一帧取最大能量（跨所有频率 bin）
    max_db_per_frame = S_db.max(axis=0)

    # 时间轴
    times = librosa.frames_to_time(
        np.arange(len(max_db_per_frame)),
        sr=sr,
        hop_length=HOP_LENGTH
    )

    # 子图
    plt.subplot(1, 1, i)
    plt.plot(times, max_db_per_frame)
    plt.ylabel("Max dB")
    plt.title(f"File {i}: max energy per frame")
    plt.ylim(-80, 0)

    if i == idx:
        plt.xlabel("Time (s)")

plt.tight_layout()
plt.show()