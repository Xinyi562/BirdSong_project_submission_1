# Discarded: unable to form all-in-one folder for output_test.
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

from utils.metadata_ready_old import metadata_ready





# 参数
threshold_db = -30
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512

filtered_df = metadata_ready()

for idx, row in filtered_df.iterrows():

    if idx >= 3:   # 测试用
        break

    AUDIO_DIR = row["full_path"]
    print("Processing:", AUDIO_DIR)

    # 1️⃣ 读取音频
    y, sr = librosa.load(AUDIO_DIR, sr=SR)

    # 2️⃣ STFT（只算一次！）
    D = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)

    # 3️⃣ 幅度
    S = np.abs(D)

    # 4️⃣ 转 dB（关键：全局最大值作为 reference）
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    # 5️⃣ 生成 mask（和 spectrogram 黑点完全一致）
    mask = S_db >= threshold_db

    # 6️⃣ 应用 mask（其余全部变 0）
    D_masked = D * mask

    # 7️⃣ 可选：重建音频（如果你想听）
    y_masked = librosa.istft(D_masked, hop_length=HOP_LENGTH)

    out_audio = f"masked_{idx}.wav"
    sf.write(out_audio, y_masked, sr)

    # 8️⃣ 保存 mask（用于后续分析）
    np.save(f"mask_{idx}.npy", mask)

    # 9️⃣ 可视化（确认和你原图一致）
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.title("Spectrogram (dB)")
    plt.imshow(S_db, aspect='auto', origin='lower')

    plt.subplot(1, 2, 2)
    plt.title("Mask (>= -30 dB)")
    plt.imshow(mask, aspect='auto', origin='lower')

    plt.tight_layout()
    plt.show()