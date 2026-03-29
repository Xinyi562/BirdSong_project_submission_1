import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import os
import pandas as pd# ✅ NEW（读CSV用）
import random

# ❌ 原来这个不要了（或可以注释掉）
# from utils.metadata_ready import metadata_ready
from utils.find_project_root import find_project_root







# 参数
threshold_db = -38
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512


# ✅ NEW：读取你的 metadata CSV
#METADATA_PATH = os.path.join("utils", "filtered_metadata_preview.csv")

# Finding root directory of the project
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

# ✅ NEW：三个输出文件夹
#OUTPUT_DIR = "output_test"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_test")
WAV_DIR = os.path.join(OUTPUT_DIR, "wav")
NPY_DIR = os.path.join(OUTPUT_DIR, "npy")
PNG_DIR = os.path.join(OUTPUT_DIR, "png")

os.makedirs(WAV_DIR, exist_ok=True)
os.makedirs(NPY_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

for idx, row in filtered_df.iterrows():

    if idx >= 1:   # 测试用
        break

    AUDIO_DIR = row["full_path"]   # ⚠️ 确保CSV里有这一列
    FILE_ID = row["file_id"]        # ✅ NEW（核心）

    print("Processing file_id:", FILE_ID)
    print("index:", idx)

    # 1️⃣ 读取音频
    #y, sr = librosa.load(AUDIO_DIR, sr=SR)
    try:
        y, sr = librosa.load(AUDIO_DIR, sr=SR)
    except Exception as e:
        print(f"Error processing {FILE_ID}: {e}")
        continue

    # 2️⃣ STFT（只算一次！）
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
    wav_path = os.path.join(WAV_DIR, f"{FILE_ID}.wav")
    sf.write(wav_path, y_masked, sr)

    npy_path = os.path.join(NPY_DIR, f"{FILE_ID}.npy")
    np.save(npy_path, mask)

    # 9️⃣ 可视化
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.title("Spectrogram (dB)")
    plt.imshow(S_db, aspect='auto', origin='lower')

    plt.subplot(1, 2, 2)
    plt.title("Mask (>= -30 dB)")
    plt.imshow(mask, aspect='auto', origin='lower')

    plt.tight_layout()

    png_path = os.path.join(PNG_DIR, f"{FILE_ID}.png")
    plt.savefig(png_path)
    plt.close()