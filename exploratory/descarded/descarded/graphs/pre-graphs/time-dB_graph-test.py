# This code was discarded since it is redundant and contains incorrect data.
import os
import random
import numpy as np
import librosa.display
import matplotlib.pyplot as plt

from utils.metadata_ready_old import filtered_dataset
#from utils.load_filtered_metadata import load_filtered_metadata
#from utils.find_project_root import find_project_root



# Finding the relative path for AUDIO_DIR.
#current_dir = os.path.dirname(os.path.abspath(__file__))
#BASE_DIR = find_project_root(__file__)
#AUDIO_DIR = os.path.join(BASE_DIR, "archive", "songs")

#BASE_DIR = find_project_root(__file__)
#METADATA_PATH = os.path.join(BASE_DIR, "archive", "birdsong_metadata.csv")
#AUDIO_FOLDER = os.path.join(BASE_DIR, "archive", "songs")

#filtered_df = load_filtered_metadata(
    #metadata_path = METADATA_PATH,
    #audio_folder = AUDIO_FOLDER,
    #lat_min=35,
    #lat_max=71,
    #lon_min=-25,
    #lon_max=65,
    #keyword="song"
#)




SR = 22050
N_FFT = 2048
HOP_LENGTH = 512
while True: # Graph index based on user input.
    try:
        idx = int(input(f"Choose between 0~{len(filtered_df) - 1}: "))
        if 0 <= idx < len(filtered_df):
            break
        else:
            print("Index out of range, try again.")
    except ValueError:
        print("Please enter an integer.")

audio_files = filtered_dataset()
# =============================
# 选音频文件
# =============================
#audio_files = [
    #os.path.join(AUDIO_DIR, f)
    #for f in os.listdir(AUDIO_DIR)
    #if f.lower().endswith((".wav", ".flac", ".mp3"))
#]

selected_files = audio_files[idx:idx + 1]
#selected_files = random.sample(audio_files, idx)
# =============================
# 画图 (只画选中的那一个文件)
# =============================
plt.figure(figsize=(8, 4))

# 1. 直接通过索引取出那个文件，不再需要 selected_files 列表
#filepath = audio_files[idx]

y, sr = librosa.load(filtered_df, sr=SR)

# STFT
S = np.abs(librosa.stft(
    y,
    n_fft=N_FFT,
    hop_length=HOP_LENGTH
))

# 转 dB
S_db = librosa.amplitude_to_db(S, ref=np.max)

# 每一帧取最大能量
max_db_per_frame = S_db.max(axis=0)

# 时间轴
times = librosa.frames_to_time(
    np.arange(len(max_db_per_frame)),
    sr=sr,
    hop_length=HOP_LENGTH
)

# 直接绘图，不需要 plt.subplot 了（默认就是一整张）
plt.plot(times, max_db_per_frame)
plt.ylabel("Max dB")
plt.xlabel("Time (s)") # 直接写，不用判断
plt.title(f"File Index {idx}: {os.path.basename(filtered_df)}")
plt.ylim(-80, 0)

plt.tight_layout()
plt.show()
