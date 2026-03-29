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







plt.figure(figsize = (8, 4))
librosa.display.specshow( #三维数据用specshow(自动帮转换为真实的Hz, 时间(s))
    S_db,                 #第一个参数用颜色表示
    sr=sr,
    x_axis="time",
    y_axis="hz",
)
# 鼠标交互显示坐标
def format_coord(x, y):
    # x 是时间(s)，y 是频率(Hz)
    # 将时间转化为列索引，频率转化为行索引
    col = np.argmin(np.abs(librosa.times_like(S_db, sr=sr, hop_length=HOP_LENGTH) - x))
    row = np.argmin(np.abs(librosa.fft_frequencies(sr=sr, n_fft=N_FFT) - y))

    try:
        z = S_db[row, col]
        return f'Time: {x:.2f}s, Freq: {y:.1f}Hz, Energy: {z:.2f}dB'
    except IndexError:
        return f'Time: {x:.2f}s, Freq: {y:.1f}Hz'

plt.gca().format_coord = format_coord

plt.colorbar(label="dB")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title(f"File {idx}: {AUDIO_DIR}")
plt.tight_layout()
plt.show()






