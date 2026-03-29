# 不小心提取了空白部分
import librosa
import numpy as np
import soundfile as sf

from utils.metadata_ready_old import metadata_ready





threshold_db = -30
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512

filtered_df = metadata_ready()
for idx, row in filtered_df.iterrows():

    if idx >= 10:   # 先测试10个
        break

    AUDIO_DIR = row["full_path"]
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





    # 每一帧是否存在 ≥ -30 dB
    active_frames = np.any(S_db >= threshold_db, axis=0) #横着的不变

    segments = []
    start = None

    for i, val in enumerate(active_frames):

        if val and start is None:
            start = i

        elif not val and start is not None:
            segments.append((start, i))
            start = None

    if start is not None:
        segments.append((start, len(active_frames)))

    # frame → sample
    hop_length = 512

    for j, (s, e) in enumerate(segments):

        start_sample = s * hop_length
        end_sample = e * hop_length

        clip = y[start_sample:end_sample]

        out_name = f"clip_{idx}_{j}.wav"

        sf.write(out_name, clip, sr)