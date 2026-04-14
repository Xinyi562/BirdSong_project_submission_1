# BirdSong Project
Testing whether a hypothesized signal (latitude-frequency relation) exists

### Project Structure:
This project consists of three parts:
- Step One: Data Filtering 
- Step Two: Visualize Frequency Distribution for Each Bird 
- Step Three: Visualize Frequency Distribution in Geographic Context

### Important Note:
Please start by reading the README in the `first` folder, which covers Step One.  
Step Two builds upon the outputs of Step One (e.g., metadata files).  


### Limitations:
- Signal Precision: Fixed parameters for Sample Rate (SR) and N_FFT were used for batch processing. Potential data loss or spectral leakage may occur during audio windowing and STFT, affecting the precision of the resulting frequency fingerprints.
- Low-Frequency Filtering: A manual high-pass adjustment is applied to clear all activity below 800 Hz in the visualizations. This is intended to eliminate environmental "hum" (e.g., wind or traffic) from field recordings, though it may hide legitimate low-frequency biological signals.
- Geographic Scope: The dataset is filtered based on estimated European coordinates (Latitude: 35°N to 71°N, Longitude: -25°W to 65°E).
- Biological Scope: Currently, the filter does not account for specific genus or species; it focuses purely on geographic range and vocalization type.
- Frequency Scope (SR): Analysis is limited to 0-11025 Hz, (using SR=22050), missing ultra-high-frequency recordings above 11KHz.
- Frequency Resolution (N_FFT): Limited to approximately 10.77 Hz, caused by the fixed N_FFT size. Closely spaced frequencies cannot be distinguished.
- Time resolution (HOP_LENGTH): Time resulution limited by a hop interval of 0.023. Rapid acoustic changes details may not be fully captured.
- Purpose: This is an exploratory tool designed for initial data visualization and filtering.