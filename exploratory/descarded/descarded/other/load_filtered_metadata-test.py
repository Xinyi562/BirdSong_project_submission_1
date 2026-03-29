# This code was discarded since it returns incorrect file names.
import pandas as pd
import os


# Filtering metadata for type 'song' + latitude 35-71 + longitute -25~65
def load_filtered_metadata(
        metadata_path,
        audio_folder,
        lat_min=35,
        lat_max=71,
        lon_min=-25,
        lon_max=65,
        keyword="song"
):
    # lat + lon + type------------------------------------------------------------------------------------------------------------------
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"找不到元数据文件: {metadata_path}")
    df = pd.read_csv(metadata_path)

    # 纬度处理
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df = df.dropna(subset=['latitude'])
    mask_lat = (df['latitude'] >= lat_min) & (df['latitude'] <= lat_max)
    #经度处理
    df['longitute'] = pd.to_numeric(df['longitute'], errors='coerce')
    df = df.dropna(subset=['longitute'])
    mask_lon = (df['longitute'] >= lon_min) & (df['longitute'] <= lon_max)
    #类型
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



    # 格式整理 + 音频存在-------------------------------------------------------------------------------------------------------------
    def get_full_path(file_id):
        # 确保 file_id 是整数或干净的字符串，避免出现 "123.0.flac"
        if isinstance(file_id, float):
            clean_id  = str(int(file_id))
        else:
            clean_id = str(file_id)
        return os.path.join(audio_folder, clean_id + ".flac")

    filtered_data['full_path'] = filtered_data['file_id'].apply(get_full_path)
    is_real = filtered_data['full_path'].apply(os.path.exists)
    final_data = filtered_data[is_real].reset_index(drop=True)


    print(f"原始数据: {len(df)} 条")
    total_criteria_dropped = len(df) - final_criteria_mask.sum()
    print(f"其中不符合要求的有: {total_criteria_dropped} 条")
    print(f"条件筛选后: {len(filtered_data)} 条")

    missing = (~filtered_data['full_path'].apply(os.path.exists)).sum()
    print(f"其中没有音频文件的有: {missing} 条")
    print(f"最终数据: {len(final_data)} 条")


    return final_data




