import pandas as pd
import os


def filter_data(
        metadata_path,
        audio_folder,
        lat_min=35,
        lat_max=71,
        lon_min=-25,
        lon_max=65,
        keyword="song"
):
    """
    Filter bird audio metadata based on geographic region and vocalization type.
 Parameters:
       metadata_path (str): Path to the metadata CSV file.
       audio_folder (str): Directory containing audio files.
       lat_min, lat_max (float): Latitude range.
       lon_min, lon_max (float): longitute range.
       keyword (str): Target vocalization type (e.g., "song").

Returns:
       pd.DataFrame: Filtered dataset with valid audio file paths.
       """




    # --- Load metadata ---
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Cannot find file: {metadata_path}")

    df = pd.read_csv(metadata_path)







    # --- data filtration ---
    # Latitude
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df = df.dropna(subset=['latitude'])
    mask_lat = (df['latitude'] >= lat_min) & (df['latitude'] <= lat_max)

    # longitute
    df['longitute'] = pd.to_numeric(df['longitute'], errors='coerce')
    df = df.dropna(subset=['longitute'])
    mask_lon = (df['longitute'] >= lon_min) & (df['longitute'] <= lon_max)

    # type
    df['type'] = df['type'].astype(str)
    mask_type = df['type'].str.contains(
        rf"\b{keyword.lower()}\b",
        na=False,
        regex=True
    )
    # Combine all filters
    final_mask = mask_lat & mask_lon & mask_type
    filtered_data = df[final_mask].copy()







    # --- Construct file paths ---
    def get_full_path(file_id):
        """Convert file_id to standardized audio file path."""
        if isinstance(file_id, float):
            clean_id = str(int(file_id))
        else:
            clean_id = str(file_id)

        filename = f"xc{clean_id}.flac"
        return os.path.join(audio_folder, filename)

    filtered_data['full_path'] = filtered_data['file_id'].apply(get_full_path)

    # Remove missing audio files
    exists_mask = filtered_data['full_path'].apply(os.path.exists)
    final_data = filtered_data[exists_mask].reset_index(drop=True)







    # --- Summary ---
    print("--------- Filter Summary ---------")
    print(f"Original samples: {len(df)}")
    print(f"After filtering: {len(filtered_data)}")

    missing = (~exists_mask).sum()
    print(f"Missing audio files: {missing}")
    print(f"Final dataset size: {len(final_data)}")
    print("----------------------------------")

    return final_data