# 花花绿绿散点图
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os
import pandas as pd
import random

from utils.find_project_root import find_project_root







BASE_DIR = find_project_root(__file__, marker=".git")
METADATA_PATH = os.path.join(BASE_DIR, "utils", "filtered_metadata_preview.csv")
if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(
        f"Metadata file not found at {METADATA_PATH}. "
        "Make sure 'utils/filtered_metadata_preview.csv' exists."
    )
filtered_df = pd.read_csv(METADATA_PATH)







# 设参数
SR = 22050 #每秒钟打点计数次数
N_FFT = 2048 #每次从SR里抓取的采样点个数
HOP_LENGTH = 512 #每隔512个点记录一次
while True:   #------Graph index based on user input.
    try:
        idx = int(input(f"Choose between 0~{len(filtered_df) - 1}: "))
        if 0 <= idx < len(filtered_df):
            break
        else:
            print("Index out of range, try again.")
    except ValueError:
        print("Please enter an integer.")

#idx = random.randint(0, len(filtered_df) - 1)  # ------OR use random numbers
AUDIO_DIR = filtered_df.loc[idx, 'full_path']
FILE_ID = filtered_df.loc[idx, "file_id"]
print("Processing file", idx,":", FILE_ID)







# 音频录入
y, sr = librosa.load(AUDIO_DIR, sr=SR)
# STFT
S = np.abs(librosa.stft(
    y,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
))
# 转 dB
S_db = librosa.amplitude_to_db(S, ref=np.max)
# 频率 & 时间轴
freqs = librosa.fft_frequencies(sr=sr, n_fft=N_FFT) # frequency bin(琴键)转换为真正的Hz
times = librosa.frames_to_time( # time frame转换为真正的时间(s)
np.arange(S_db.shape[1]),
    sr=sr,
    hop_length=HOP_LENGTH
)
#对齐数据坐标
T, F = np.meshgrid(times, freqs)
# 展开数据, 方便画图
t_flat = T.flatten()
f_flat = F.flatten()
db_flat = S_db.flatten()





# 抽样画图, 防止死机
sample_idx = np.random.choice(
    len(db_flat),
    size= min(100_000, len(db_flat)), # 抽样只抽最多100000个点
    replace=False
)
t_plot = t_flat[sample_idx]
f_plot = f_flat[sample_idx]
db_plot = db_flat[sample_idx]

#作图开始
plt.figure(figsize=(8, 4))
sc = plt.scatter(
    t_plot, # 横坐标
    db_plot,# 纵坐标
    c=f_plot,# 颜色表示
    s=1,     #每个点大小
    alpha=0.3,#透明度
    cmap="viridis"# 高频低频对应不同颜色
)
plt.colorbar(sc, label="Frequency (Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Energy (dB)")
plt.title(f"File {idx}: {AUDIO_DIR}")

plt.ylim(-80, 0) # 固定Y轴范围
plt.show() #作图结束