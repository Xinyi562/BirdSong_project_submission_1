# Step two: filter birdsong base on threshold dB + visualize frequency distribution

### Note: 
- metadata file (filtered_metadata_preview.csv) is excluded from this repository.
To run the project, please run the generate_CSV.py in utils to generate a new csv under /utils/
- Ensure you have the following libraries installed:
`pip install librosa numpy matplotlib pandas`

### Limitations & Scope:
- Threshold Arbitrariness: The signal-to-noise separation relies on a fixed threshold (-30 dB), which was determined by empirical estimation. This may incorrectly classify loud background noise as vocalization or omit faint bird calls.
- Signal Precision: Fixed parameters for Sample Rate (SR) and N_FFT were used for batch processing. Potential data loss or spectral leakage may occur during audio windowing and STFT, affecting the precision of the resulting frequency fingerprints.
- Low-Frequency Filtering: A manual high-pass adjustment is applied to clear all activity below 200 Hz in the visualizations. This is intended to eliminate environmental "hum" (e.g., wind or traffic) from field recordings, though it may hide legitimate low-frequency biological signals.
- Geographic Scope: The dataset is filtered based on estimated European coordinates (Latitude: 35°N to 71°N, Longitude: -25°W to 65°E).
- Biological Scope: Currently, the filter does not account for specific genus or species; it focuses purely on geographic range and vocalization type.
- Purpose: This is an exploratory tool designed for initial data visualization and filtering.

### Core Scripts
- filterby_dB_inputRange_png.py: The varification entry point. It processes audio files from the metadata and generates side-by-side comparisons of original spectrograms and binary masks to verify threshold effectiveness.
- plot_band.py: Another visualization entry point built on filterby_dB_inputRange_png.py. It converts filtered audio files into high-contrast frequency "fingerprints" by collapsing the time axis to highlight dominant spectral activity.

### exploratory
A subset of audio samples was manually reviewed to qualitatively assess noise reduction and preservation of birdsong signals.