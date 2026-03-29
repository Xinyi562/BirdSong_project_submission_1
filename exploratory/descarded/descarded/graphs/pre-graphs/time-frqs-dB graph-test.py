#This code was discarded since it includes redundancy.
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from utils.find_project_root import find_project_root

# =============================
# 音频文件夹路径
# =============================
#AUDIO_DIR = r"/archive/songs/songs"
BASE_DIR = find_project_root(__file__)
AUDIO_DIR = os.path.join(BASE_DIR, "archive", "songs")

idx = 119

# 取所有 wav 文件

audio_files = [
    f for f in os.listdir(AUDIO_DIR)
    if f.lower().endswith((".wav", ".flac", ".mp3"))
]

# 只取前 10 个
audio_files = audio_files[idx:idx + 1]

print(f"Will plot {len(audio_files)} files")

# =============================
# 逐个画图
# =============================
for i, filename in enumerate(audio_files, start=1):
    file_path = os.path.join(AUDIO_DIR, filename)

    # 读音频（原始，不裁）
    y, sr = librosa.load(file_path, sr=None)

    # STFT → 幅度 → dB
    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    # 画图
    plt.figure()
    librosa.display.specshow(
        S_db,
        sr=sr,
        x_axis="time",
        y_axis="hz"
    )
    plt.colorbar(label="dB")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(f"{i}: {filename}")
    plt.tight_layout()
    plt.show()