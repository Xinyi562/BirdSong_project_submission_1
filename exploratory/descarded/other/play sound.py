# Discarded: Not showing progress / cannot adjust progress accordingly
import os
import librosa
import sounddevice as sd

from utils.metadata_ready_old import filtered_dataset
from utils.find_project_root import find_project_root



BASE_DIR = find_project_root(__file__)
AUDIO_FOLDER = os.path.join(BASE_DIR, "archive", "songs")
filtered_df = filtered_dataset()

#AUDIO_DIR = r"/archive/songs/songs"
SR = 22050
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


# 找到第一个 flac 文件
audio_files = [
    f for f in os.listdir(AUDIO_FOLDER)
    if f.lower().endswith(".flac")
]

play_file = audio_files[85]
file_path = os.path.join(AUDIO_FOLDER, play_file)

print("Playing:", play_file)

# 读音频（不裁、不滤）
y, sr = librosa.load(file_path, sr=SR, mono=True)

# 播放
sd.play(y, sr)
sd.wait()
