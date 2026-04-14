# Step two
filter birdsong base on threshold dB + visualize frequency distribution

### Note: 
- metadata file (filtered_metadata_preview.csv) is excluded from this repository.
To run the project, please run the generate_CSV.py in utils to generate a new csv under /utils/
- Ensure you have the following libraries installed:
`pip install librosa numpy matplotlib pandas`

### Core Scripts
- filterby_dB_inputRange_png.py: The varification entry point. It processes audio files from the metadata and generates side-by-side comparisons of original spectrograms and binary masks to verify threshold effectiveness.
- plot_band.py: Another visualization entry point built on filterby_dB_inputRange_png.py. It converts filtered audio files into high-contrast frequency "fingerprints" by collapsing the time axis to highlight dominant spectral activity.

### Limitations:
(See main README for overall shared limitation)
- Threshold Arbitrariness: The signal-to-noise separation relies on a fixed threshold (-30 dB), which was determined by empirical estimation. This may incorrectly classify loud background noise as vocalization or omit faint bird calls.


### exploratory
A subset of audio samples was manually reviewed to qualitatively assess noise reduction and preservation of birdsong signals.