# this code was discarded since it contains redundancy.
import numpy as np
import librosa
import matplotlib.pyplot as plt
import os

from utils.metadata_ready_old import filtered_dataset
#from utils.find_project_root import find_project_root



#找文件
    #BASE_DIR = find_project_root(__file__)
    #METADATA_PATH = os.path.join(BASE_DIR, "archive", "birdsong_metadata.csv")
    #AUDIO_FOLDER = os.path.join(BASE_DIR, "archive", "songs")
filtered_df = filtered_dataset()


# 设参数
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



AUDIO_DIR = filtered_df.loc[idx, 'full_path']
print("Using filtered file:", AUDIO_DIR)


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

max_db_per_frame = S_db.max(axis=0)

times = librosa.frames_to_time(
    np.arange(len(max_db_per_frame)),
    sr=sr,
    hop_length=HOP_LENGTH
)

plt.plot(times, max_db_per_frame)
plt.ylabel("Max dB")
plt.xlabel("Time (s)") # 直接写，不用判断
#plt.title(f"File Index {idx}: {str(os.path.basename(filtered_df))}")
plt.title(f"File Index {idx}: {os.path.basename(AUDIO_DIR)}")
plt.ylim(-80, 0)

plt.tight_layout()
plt.show()