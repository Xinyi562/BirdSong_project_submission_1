# This code was discarded since it fail to integrate some key constrains.
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt

# -----------------------------
# 参数
# -----------------------------
data_dir = r"D:\British_BirdSong_dataSet\archive\songs\songs"  # 修改为你的 songs 文件夹路径
percentile = 85  # 能量覆盖百分比

# -----------------------------
# 函数：计算音频频率分布
# -----------------------------
def compute_frequency_distribution(file_path):
    """
    输入: 单个音频文件路径
    输出: freqs, total_energy
    """
    y, sr = librosa.load(file_path, sr=None)  # 直接读取 .flac
    S = np.abs(librosa.stft(y))
    energy = np.sum(S, axis=1)  # 每个频率 bin 的能量
    freqs = librosa.fft_frequencies(sr=sr)
    return freqs, energy

# -----------------------------
# 函数：计算 85% 能量带
# -----------------------------
def compute_energy_band(freqs, energy, percentile=85):
    cumulative = np.cumsum(energy) / np.sum(energy)
    low_idx = np.searchsorted(cumulative, (1 - percentile/100)/2)
    high_idx = np.searchsorted(cumulative, 1 - (1 - percentile/100)/2)
    f_low = freqs[low_idx]
    f_high = freqs[high_idx]
    return f_low, f_high

# -----------------------------
# 批量处理每只鸟
# -----------------------------
bird_files = [f for f in os.listdir(data_dir) if f.endswith(".flac")]

output_dir = "D:/birdsong_project/output_test"
os.makedirs(output_dir, exist_ok=True)

bird_bands = {}  # 保存每只鸟的 85% 能量带

for bird_file in bird_files:
    file_path = os.path.join(data_dir, bird_file)
    freqs, energy = compute_frequency_distribution(file_path)
    f_low, f_high = compute_energy_band(freqs, energy, percentile)
    bird_bands[bird_file] = (f_low, f_high)

    # -----------------------------
    # 绘制渐变色频率分布
    # -----------------------------
    plt.figure(figsize=(4, 6))
    alpha_values = energy / np.max(energy)  # 能量归一化 → 渐变
    for f, a in zip(freqs, alpha_values):
        plt.fill_between([0, 1], [f, f], [f+1, f+1], color='blue', alpha=a)

    plt.title(f"{bird_file} Frequency Distribution")
    plt.xlabel("Amplitude")
    plt.ylabel("Frequency (Hz)")
    plt.xticks([])
    plt.tight_layout()
