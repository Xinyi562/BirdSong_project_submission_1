# Step three
Latitude-partitioned frequency overlay visualization based on user-defined percentage bins

### Note: 
- metadata file (filtered_metadata_preview.csv) is excluded from this repository.
To run the project, please run the generate_CSV.py in utils to generate a new csv under /utils/
- Ensure you have the following libraries installed:
`pip install librosa numpy matplotlib pandas`

### Core Scripts
- distribution_plot.py: Main visualization entry built upon filtered audio frequency extraction. The script accepts custom latitude percentage partitions from user input, assigns each audio to corresponding latitude bins, accumulates normalized spectral density, and generates concatenated group-wise frequency overlay plots.

### Limitations:
(See main README for overall shared limitation)
- Threshold Arbitrariness: The signal-to-noise separation relies on a fixed threshold (-30 dB), which was determined by empirical estimation. This may incorrectly classify loud background noise as vocalization or omit faint bird calls.
- Within-Group Comparison Only: Visual brightness reflects only within-group relative frequency peaks, not sample count. Group size differences cannot be identified from plot brightness.
- Uneven Sample Distribution: Due to sparse bird distribution, some latitude bins contain nearly zero samples, resulting in blank regions in the visualization. Additionally, group sizes vary drastically—some have only 5-6 valid samples, while others contain over 200, creating unbalanced visual contrast across bins.

### exploratory
A subset of audio samples was manually reviewed to qualitatively assess noise reduction and preservation of birdsong signals.