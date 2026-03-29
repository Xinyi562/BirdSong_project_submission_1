# Discarded: not proper formated + redundancy
# originally in utils

# Filter original metadata's latitude (35~71), longitute(-25~65), and intended birdsong type('song').
# Based on estimated European geographical data.
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

    # Data filtering------------------------------------------------------------------------------------------------------------------
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"cannot find file: {metadata_path}")
    df = pd.read_csv(metadata_path)


     # latitude filtering
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df = df.dropna(subset=['latitude'])
    mask_lat = (df['latitude'] >= lat_min) & (df['latitude'] <= lat_max)
    # longitute filtering
    df['longitute'] = pd.to_numeric(df['longitute'], errors='coerce')
    df = df.dropna(subset=['longitute'])
    mask_lon = (df['longitute'] >= lon_min) & (df['longitute'] <= lon_max)
    # type filtering
    df['type'] = df['type'].astype(str)
    mask_type = df['type'].str.contains(
        rf"\b{keyword.lower()}\b",#有单个song单词
        na=False, #缺失值返回false
        regex=True#只要单个song单词
    )

    final_criteria_mask = mask_lat & mask_lon & mask_type
    filtered_data = (
        df[final_criteria_mask]
        .copy()
    )







    # formating + deleting invalid data-------------------------------------------------------------------------------------------------------------
    def get_full_path(file_id):
        # Make sure file_id is int or string，avoid instance such as "123.0.flac"
        if isinstance(file_id, float):
            clean_id = str(int(file_id))
        else:
            clean_id = str(file_id)

        filename = f"xc{clean_id}.flac"
        return os.path.join(audio_folder, filename)

    # Adding "full_path" colum into metadata
    filtered_data['full_path'] = filtered_data['file_id'].apply(get_full_path)



    is_real = filtered_data['full_path'].apply(os.path.exists)
    final_data = filtered_data[is_real].reset_index(drop=True)







    print("---------printing filtered results------------")
    print(f"original file count: {len(df)} ")
    #total_criteria_dropped = len(df) - final_criteria_mask.sum()
    #print(f"unqualified data: {total_criteria_dropped} ")
    print(f"files after filtering: {len(filtered_data)} ")
    print()
    missing = (~filtered_data['full_path'].apply(os.path.exists)).sum()
    print(f"files without audio: {missing} ")
    print(f"final filtered files count: {len(final_data)}")
    print("----------------------------------------------")

    return final_data





