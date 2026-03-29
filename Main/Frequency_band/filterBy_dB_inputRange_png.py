import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from utils.find_project_root import find_project_root







# --- Global Configurations ---
# Audio processing parameters
threshold_db = -30
SR = 22050
N_FFT = 2048
HOP_LENGTH = 512

# Path Setup
BASE_DIR = find_project_root(__file__, marker="archive")
METADATA_PATH = os.path.join(BASE_DIR, "utils", "filtered_metadata_preview.csv")
# Ensure metadata exists to prevent runtime errors
if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(
        f"Metadata file not found at {METADATA_PATH}. "
        "Make sure 'utils/filtered_metadata_preview.csv' exists."
    )

filtered_df = pd.read_csv(METADATA_PATH)
OUTPUT_DIR = os.path.join(BASE_DIR, "output_test")
PNG_DIR = os.path.join(OUTPUT_DIR, "png")
os.makedirs(PNG_DIR, exist_ok=True)


# User Input for Batch Processing
print(f"Enter index between 1 ~ {len(filtered_df)}")
start_idx = int(input("Enter start index(inclusive): "))
end_idx = int(input("Enter end index (inclusive): "))

# Ensure input in index range
if start_idx < 1 or end_idx > len(filtered_df) or start_idx > end_idx:
    raise ValueError("Invalid range input. Range must be 1 to {len(filtered_df)}.")

# Slice dataframe based on user input
filtered_df = filtered_df.iloc[start_idx - 1:end_idx]







# --- Main Processing Loop ---
for idx, row in filtered_df.iterrows():
    AUDIO_DIR = row["full_path"]
    FILE_ID = row["file_id"]
    print("Processing file", idx + 1, ":", FILE_ID)

    try:
        # Load audio file with fixed sampling rate
        y, sr = librosa.load(AUDIO_DIR, sr=SR)
    except Exception as e:
        print(f"Error processing {FILE_ID}: {e}")
        continue

    # 1. Feature Extraction: STFT and Decibel conversion
    D = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    # 2. Binary Masking: Identify active frequency components
    mask = S_db >= threshold_db
    # mask sounds under 200 Hz
    cutoff_bin = int(200 * N_FFT / SR)
    S_db[:cutoff_bin, :] = np.min(S_db)
    mask[:cutoff_bin, :] = False

    # 3. Audio Reconstruction (Optional): Apply mask to complex STFT
    # Multiplying the mask effectively removes noise below the threshold
    D_masked = D * mask
    # Perform inverse STFT to convert back to time-domain audio signal
    y_masked = librosa.istft(D_masked, hop_length=HOP_LENGTH)







    # --- Visual Rendering ---
    # Left subplot: Original Spectrogram in dB
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.title("Spectrogram (dB)")
    plt.imshow(S_db, aspect='auto', origin='lower')

    # Right subplot: Visualization of the Binary Mask
    plt.subplot(1, 2, 2)
    plt.title(f"Mask (>= {threshold_db} dB)")
    plt.imshow(mask, aspect='auto', origin='lower')

    plt.tight_layout()






    # --- Save and Cleanup ---
    png_path = os.path.join(PNG_DIR, f"{idx + 1}_{FILE_ID}.png")
    plt.savefig(png_path)
    plt.close()