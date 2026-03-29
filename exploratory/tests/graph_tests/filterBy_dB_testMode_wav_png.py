import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import os
import pandas as pd

from utils.find_project_root import find_project_root







# 参数
TARGET_INDEX = 4
TEST_MODE = True
threshold_db = -30
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512

BASE_DIR = find_project_root(__file__, marker=".git")
# ✅ 拼接 metadata 路径（跨电脑可用）
METADATA_PATH = os.path.join(BASE_DIR, "utils", "filtered_metadata_preview.csv")
# ✅ 优雅报错（防止教授运行炸掉还不知道原因）
if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(
        f"Metadata file not found at {METADATA_PATH}. "
        "Make sure 'utils/filtered_metadata_preview.csv' exists."
    )
filtered_df = pd.read_csv(METADATA_PATH)

OUTPUT_DIR = os.path.join(BASE_DIR, "output_test")
WAV_DIR = os.path.join(OUTPUT_DIR, "wav")
PNG_DIR = os.path.join(OUTPUT_DIR, "png")

os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(WAV_DIR, exist_ok=True)








if TARGET_INDEX is not None:
    if TARGET_INDEX >= len(filtered_df):
        raise ValueError("TARGET_INDEX out of range")
    filtered_df = filtered_df.iloc[[TARGET_INDEX]]

elif TEST_MODE:
    filtered_df = filtered_df.sample(n=1)


for idx, row in filtered_df.iterrows():

    AUDIO_DIR = row["full_path"]   # ⚠️ 确保CSV里有这一列
    FILE_ID = row["file_id"]        # ✅ NEW（核心）
    print("Processing file", idx, ":", FILE_ID)

    try:
        y, sr = librosa.load(AUDIO_DIR, sr=SR)
    except Exception as e:
        print(f"Error processing {FILE_ID}: {e}")
        continue

    D = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)
    # 3️⃣ 幅度
    S = np.abs(D)
    # 4️⃣ 转 dB
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    # 5️⃣ mask
    mask = S_db >= threshold_db
    # 6️⃣ 应用 mask
    D_masked = D * mask
    # 7️⃣ 重建音频
    y_masked = librosa.istft(D_masked, hop_length=HOP_LENGTH)

    # ✅ 用 file_id 命名
    wav_path = os.path.join(WAV_DIR, f"{idx}_{FILE_ID}.wav")
    sf.write(wav_path, y_masked, sr)

    # 9️⃣ 可视化
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.title("Spectrogram (dB)")
    plt.imshow(S_db, aspect='auto', origin='lower')

    plt.subplot(1, 2, 2)
    plt.title(f"Mask (>= {threshold_db} dB)")
    plt.imshow(mask, aspect='auto', origin='lower')

    plt.tight_layout()

    png_path = os.path.join(PNG_DIR, f"{idx}_{FILE_ID}.png")
    plt.savefig(png_path)
    plt.close()