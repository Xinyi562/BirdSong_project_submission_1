# 蓝线图
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
y, sr = librosa.load(AUDIO_DIR, sr=SR) #返回NUmPy array, Y:每一个采样点的振幅
# STFT
S = np.abs(librosa.stft( # 用SR,N_FFT, HOP_LENGTH真的动起来. abs: 复数绝对值得到振幅
    y,                   # 复数: 钢琴键竖着放. 列:time frame (not frame index); 行:每一个琴音(是否被按响,有多响)
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
))
# 振幅转 dB
S_db = librosa.amplitude_to_db(S, ref=np.max) # ref: dB是比出来的,不是算出来的; 强制对齐,增加可比度 (最小值无限小)
max_db_per_frame = S_db.max(axis=0) #提取每一坨的dB最大值
times = librosa.frames_to_time(       #算出每一个点是在多少秒
    np.arange(len(max_db_per_frame
    )), #给刚刚的最大值编号
    sr=sr,
    hop_length=HOP_LENGTH)







plt.figure(figsize = (8, 4))
plt.plot(times, max_db_per_frame)
plt.ylabel("Max dB")
plt.xlabel("Time (s)")
plt.title(f"File {idx}: {AUDIO_DIR}")
plt.ylim(-80, 0) #固定Y轴范围
plt.tight_layout() #自动排版
plt.show()