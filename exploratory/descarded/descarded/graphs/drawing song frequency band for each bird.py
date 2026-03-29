# This code was discarded since it includes unnecessary complexities.

import os
import numpy as np
import pandas as pd
import librosa
import matplotlib.pyplot as plt


AUDIO_DIR = r"/archive/songs/songs"
OUTPUT_CSV = r"D:\British_BirdSong_dataSet\birdSong_frequencyBands\results.csv"
PLOT_OUTPUT_DIR = r"D:\British_BirdSong_dataSet\birdSong_plots"
if not os.path.exists(PLOT_OUTPUT_DIR):
    os.makedirs(PLOT_OUTPUT_DIR)


SR = 22050          # 统一采样率
N_FFT = 2048        # 窗户数量
HOP_LENGTH = 512    #车厢间隔

MIN_FREQ = 500
EPS_RATIO = 0.02

def compute_frequency_activity(file_path):
    """
    返回：
    freqs          : 频率轴（Hz）
    activity_count : 每个频率被鸟使用的次数（用于颜色深浅）
    """
    y, sr = librosa.load(file_path, sr=SR, mono=True)

    # STFT 幅值谱
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)

    # 1️⃣ 去掉明显非鸟的低频
    valid = freqs >= MIN_FREQ
    S = S[valid, :]
    freqs = freqs[valid]

    # 2️⃣ 去掉“几乎是静音”的点（底噪，不是排序）
    eps = EPS_RATIO * S.max()
    active = S > eps

    # 3️⃣ 统计每个频率出现次数
    activity_count = np.sum(active, axis=1)

    return freqs, activity_count


def plot_frequency_band(freqs, activity_count, title, save_path):
    plt.figure(figsize=(4, 8))

    # 归一化 → 颜色深浅
    alpha = activity_count / activity_count.max()

    for f, a in zip(freqs, alpha):
        if a > 0:
            plt.fill_between([0, 1], f, f + 1,
                             color='blue', alpha=a)

    plt.ylim(freqs.min(), freqs.max())
    plt.xticks([])
    plt.ylabel("Frequency (Hz)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


results = []

audio_files = [
    f for f in os.listdir(AUDIO_DIR)
    if f.lower().endswith(".flac")
]

print(f"Found {len(audio_files)} audio files.")

for i, file_name in enumerate(audio_files):
    file_path = os.path.join(AUDIO_DIR, file_name)

    try:
        freqs, activity = compute_frequency_activity(file_path)

        # 保存图片
        img_name = file_name.replace(".flac", "_band.png")
        save_path = os.path.join(PLOT_OUTPUT_DIR, img_name)

        plot_frequency_band(
            freqs,
            activity,
            title=file_name,
            save_path=save_path
        )

        # 统计一个“频率范围”（仅用于表格，不裁图）
        active_freqs = freqs[activity > 0]

        results.append({
            "filename": file_name,
            "f_low_hz": active_freqs.min(),
            "f_high_hz": active_freqs.max(),
            "bandwidth_hz": active_freqs.max() - active_freqs.min()
        })

    except Exception as e:
        print(f"[ERROR] {file_name}: {e}")

    if i % 20 == 0:
        print(f"Processed {i}/{len(audio_files)}")


df = pd.DataFrame(results)
df.to_csv(OUTPUT_CSV, index=False)

print("Done.")
print(df.head())





