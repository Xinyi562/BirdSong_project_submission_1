# Discarded: formating issues
# Originally ran in utils

# Apply METADATA_PATH and AUDIO_FOLDER to filter_data function
import os
from utils.filter_data import filter_data
from utils.find_project_root import find_project_root

def metadata_ready():
    BASE_DIR = find_project_root(__file__)
    METADATA_PATH = os.path.join(BASE_DIR, "archive", "birdsong_metadata.csv")
    AUDIO_FOLDER = os.path.join(BASE_DIR, "archive", "songs")

    return filter_data(
        metadata_path=METADATA_PATH,
        audio_folder=AUDIO_FOLDER,
        lat_min=35,
        lat_max=71,
        lon_min=-25,
        lon_max=65,
        keyword="song"
    )