# Step one
data filtering + generate new CSV

### Note: Audio files (.flac) are excluded from this repository due to their large size.
To run the project, please download the dataset and place all .flac files into the following directory:
<your-project-folder>/archive/songs/

### Core Scripts
- generate_CSV.py: The main entry point. It calls the filtering logic to generate and save a new, cleaned CSV table for later analysis.
- metadata_ready.py: Constructs necessary paths and prepares the metadata for the CSV generator.
- filter_data.py: Filters by Latitude/Longitude and vocalization type (e.g., "song") + normalizes file paths and performs a physical check to drop records with missing audio files.
- find_project_root.py: A path-finding utility that searches upward from the current file to locate the project root, ensuring the code runs correctly regardless of the execution environment.
- __init__.py: A standard Python file that marks the utils directory as a package, enabling clean imports across the project.

### Limitations & Scope:
- Geographic Scope: The dataset is filtered based on estimated European coordinates (Latitude: 35°N to 71°N, Longitude: -25°W to 65°E).
- Biological Scope: Currently, the filter does not account for specific genus or species; it focuses purely on geographic range and vocalization type.
- Purpose: This is an exploratory tool designed for initial data cleaning.

