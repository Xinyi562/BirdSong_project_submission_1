import matplotlib
import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from utils.find_project_root import find_project_root







# --- Global Configurations ---
matplotlib.use('Agg') # No interactive window output

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

    # 3. Density Calculation: Sum active frames across time axis
    # Counts how many times each frequency bin exceeds the threshold
    frequency_occurrence_count = np.sum(mask, axis=1)
    max_count = np.max(frequency_occurrence_count)
    # Normalize to range[0, 1] relative to the maximum activity
    density_normalized = frequency_occurrence_count / max_count if max_count > 0 else frequency_occurrence_count

    # 4. Data Formatting: Reshape 1D data into a 2D "band" for visualization
    # and tile it horizontally to create a 2D image "band"
    density_image_data = np.tile(density_normalized.reshape(-1, 1), (1, 300))
    freqs = librosa.fft_frequencies(sr=SR, n_fft=N_FFT)







    # --- Visual Rendering ---
    FIG_COLOR = '#12012C' # Deep midnight purple background
    plt.figure(figsize=(10, 4), facecolor=FIG_COLOR)

    interp_mode  = 'bilinear'# Enable smooth color transitions between pixels

    # Draw the density fingerprint
    # Using 'plasma' colormap for high-contrast neon effect
    plt.imshow(density_image_data, # Show where to plot
               aspect='auto', # rectangular shape
               origin='lower', # The origin signed at lower left corner
               cmap='plasma', # Use 'plasma' color combination
               interpolation=interp_mode,
               #'nearest', # maintains a raw pixel integrity
               extent=[0, 1, freqs[0], freqs[-1]]) # x,y axis range

    # Access the axes object and unify its background color with the figure
    ax = plt.gca()
    ax.set_facecolor(FIG_COLOR)

    # Remove the plot borderlines (spines) for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Axis and Label Styling
    #plt.ylim(0, 8000)  # Cutting away frequency above 8000
    plt.ylabel("Frequency (Hz)", color='white', fontsize=10)
    plt.tick_params(axis='y', colors='white', length=0)
    plt.xticks([]) # Hide x-axis as time is collapsed
    plt.title(f"Frequency Density Fingerprint ({idx + 1}_{FILE_ID})", color='white', fontsize=12)
    plt.tight_layout()






    # --- Save and Cleanup ---
    png_path = os.path.join(PNG_DIR, f"{idx + 1}_{FILE_ID}_freqsBand.png")
    plt.savefig(png_path, facecolor=FIG_COLOR, bbox_inches='tight', dpi=150)
    plt.close() # release memory after each iteration

print("\nProcessing complete. Density fingerprint images saved to:", PNG_DIR)
