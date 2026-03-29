import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from utils.find_project_root import find_project_root

# 参数
threshold_db = -30
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512

BASE_DIR = find_project_root(__file__, marker=".git")
METADATA_PATH = os.path.join(BASE_DIR, "utils", "filtered_metadata_preview.csv")

if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(
        f"Metadata file not found at {METADATA_PATH}. "
        "Make sure 'utils/filtered_metadata_preview.csv' exists."
    )
filtered_df = pd.read_csv(METADATA_PATH)

OUTPUT_DIR = os.path.join(BASE_DIR, "output_test")
PNG_DIR = os.path.join(OUTPUT_DIR, "png")

os.makedirs(PNG_DIR, exist_ok=True)

print(f"Total files: {len(filtered_df)}")
start_idx = int(input("Enter start index (inclusive): "))
end_idx = int(input("Enter end index (inclusive): "))

if start_idx < 0 or end_idx >= len(filtered_df) or start_idx > end_idx:  # 修正了索引越界问题
    raise ValueError("Invalid range input. Please ensure start_idx <= end_idx and within dataframe bounds.")

# 只保留指定范围
filtered_df = filtered_df.iloc[start_idx: end_idx + 1]

for idx, row in filtered_df.iterrows():
    AUDIO_DIR = row["full_path"]
    FILE_ID = row["file_id"]
    print("Processing file", idx, ":", FILE_ID)

    try:
        y, sr = librosa.load(AUDIO_DIR, sr=SR)
    except Exception as e:
        print(f"Error processing {FILE_ID}: {e}")
        continue

    D = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)
    S = np.abs(D)
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    mask = S_db >= threshold_db

    # --- 视觉欺骗法：生成频率密度指纹图 ---
    # 1. 统计每个频率在时间轴上出现的总次数 (超过阈值的帧数)
    frequency_occurrence_count = np.sum(mask, axis=1)

    # 2. 归一化，将计数转换为 0-1 之间的密度值 (用于颜色深浅)
    # 避免除以零的情况
    max_count = np.max(frequency_occurrence_count)
    if max_count > 0:
        density_normalized = frequency_occurrence_count / max_count
    else:
        density_normalized = frequency_occurrence_count  # 全0则保持全0

    # 3. 将一维密度数组转换为二维图像数据 (高度为频率数，宽度为1或少量像素)
    # .reshape(-1, 1) 将 (N,) 变为 (N, 1)，适合 imshow 显示为垂直条
    stretch_width = 200
    density_image_data = np.tile(
        density_normalized.reshape(-1, 1),
        (1, stretch_width)    )
    #density_image_data = density_normalized.reshape(-1, 1)

    # 4. 可视化
    plt.figure(figsize=(10, 3)) # 设置一个窄长的图，适合“指纹”效果
    interpolation = 'bilinear'
    # 使用 imshow 绘制密度图
    # cmap='Greys' 或 'Blues' 让密度高的区域颜色更深
    # interpolation='nearest' 保持像素清晰，避免模糊
    # extent 用于设置 Y 轴刻度为实际频率

    # 获取频率刻度 (Hz)
    freqs = librosa.fft_frequencies(sr=SR, n_fft=N_FFT)
    # ymax = sr / 2 是 STFT 的最大频率
    # 修改这里的 cmap 参数
    # 'magma': 黑紫 -> 红 -> 橘黄 (推荐，最像你要的效果)
    # 'inferno': 黑 -> 红 -> 黄
    # 'plasma': 紫 -> 蓝 -> 黄
    plt.imshow(density_image_data,
               aspect='auto',
               origin='lower',
               cmap='plasma',  # 核心修改：换成火岩色调
               interpolation='nearest',
               extent=[0, 1, freqs[0], freqs[-1]])



    # plt.imshow(density_image_data,
    #            aspect='auto',
    #            origin='lower',
    #            cmap='Greys',  # 密度越高颜色越深
    #            interpolation='nearest',
    #            extent=[0, 1, freqs[0], freqs[-1]])  # extent: [xmin, xmax, ymin, ymax]


    # 让坐标轴文字变白，否则深色背景看不清
    plt.tick_params(axis='y', colors='white')
    plt.ylabel("Frequency (Hz)", color='white')
    plt.title(f"Frequency Density Fingerprint ({idx}_{FILE_ID})", color='white', fontsize=12)

    # 1. 先抓取当前的坐标轴对象
    ax = plt.gca()

    # 2. 现在就可以操作 ax.spines 了
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 3. 顺便把坐标轴的小短杠（刻度线）也藏起来，只留数字
    ax.tick_params(axis='y', colors='white', length=0)

    plt.xticks([])
    plt.tight_layout()

    # 保存时指定背景色，否则保存出的图片周围可能是白色的
    png_path = os.path.join(PNG_DIR, f"{idx}_{FILE_ID}density.png")
    plt.savefig(png_path, facecolor='#12012C', bbox_inches='tight')
    plt.close()

    # # 移除 X 轴刻度和标签
    # plt.xticks([])
    # # 设置 Y 轴标签
    # plt.ylabel("Frequency (Hz)")
    # plt.title(f"Frequency Density ({threshold_db} dB)")
    #
    # plt.tight_layout()
    #
    # # 保存图片
    # png_path = os.path.join(PNG_DIR, f"{idx}_{FILE_ID}_density_fingerprint.png")
    # plt.savefig(png_path)
    # plt.close()

print("\nProcessing complete. Density fingerprint images saved to:", PNG_DIR)

