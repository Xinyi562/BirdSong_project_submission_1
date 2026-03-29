# Discarded: Did not create multiple output_test files; did not use relative paths.
import librosa
import numpy as np
import os
import soundfile as sf

from utils.metadata_ready_old import metadata_ready





filtered_df = metadata_ready()
# 输入音频文件夹
#input_folder = "your_audio_folder"

# 输出剪辑后的音频
output_folder = "Birdsong_dB_filter"
os.makedirs(output_folder, exist_ok=True) #如果没有,就自己创建一个

# dB threshold
threshold_db = 30

# frame size
frame_length = 2048
hop_length = 512

#for file in os.listdir(filtered_df):
for idx, row in filtered_df.iterrows():

    if idx >= 10: #只画前10个
        break



    file_path = row["full_path"]
    y, sr = librosa.load(file_path, sr=None)

    # 计算RMS能量
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

    # 转换成dB
    db = librosa.amplitude_to_db(rms, ref=np.max)

    # 找到超过阈值的位置
    active = db >= threshold_db

    segments = []
    start = None

    for i, val in enumerate(active):
        if val and start is None:
            start = i
        elif not val and start is not None:
            end = i
            segments.append((start, end))
            start = None

    # 如果最后一段没结束
    if start is not None:
        segments.append((start, len(active)))

    # 把frame位置变成sample位置并剪音频
    for j, (s, e) in enumerate(segments):
        start_sample = s * hop_length
        end_sample = e * hop_length

        clip = y[start_sample:end_sample]

        output_path = os.path.join(
            output_folder,
            f"{file[:-4]}_bird_{j}.wav"
        )

        sf.write(output_path, clip, sr)

print("All bird calls extracted!")