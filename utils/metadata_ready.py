import os
from utils.filter_data import filter_data
from utils.find_project_root import find_project_root






def metadata_ready():
    """
    Prepare and filter birdsong metadata for downstream analysis.

    This function:
    1. Locates the project root directory
    2. Constructs paths to the metadata file and audio folder
    3. Filters the dataset based on geographic bounds and keyword

    Returns:
        pd.DataFrame: Filtered metadata containing only relevant birdsong samples
    """




    # --- locate directory---
    # Locate the root directory of the project
    base_dir = find_project_root(__file__)

    # Define path to metadata CSV file
    metadata_path = os.path.join(base_dir, "archive", "birdsong_metadata.csv")

    # Define path to folder containing audio files
    audio_folder = os.path.join(base_dir, "archive", "songs")







    # --- Apply filtering---
    # - Latitude range: Europe (approx. 35°N to 71°N)
    # - Longitude range: Europe (approx. -25° to 65°)
    # - Keep only "song" audios
    filtered_metadata = filter_data(
        metadata_path=metadata_path,
        audio_folder=audio_folder,
        lat_min=35,
        lat_max=71,
        lon_min=-25,
        lon_max=65,
        keyword="song"
    )

    return filtered_metadata