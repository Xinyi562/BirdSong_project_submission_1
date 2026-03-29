# This code was discarded since it lack key contents.
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
        song_type="song"
):
    # 增加一个路径检查，防止文件不存在报错
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

    # 使用 .str.contains 或 ==，如果是准确匹配用 ==
    mask_type = (df['type'] == song_type)

    filtered_data = df[mask_lat & mask_type & mask_lon].copy()

    file_col = 'file_id'

    def get_full_path(file_id):
        # 确保 file_id 是整数或干净的字符串，避免出现 "123.0.flac"
        clean_id = str(int(file_id)) if isinstance(file_id, float) else str(file_id)
        filename = clean_id + ".flac"
        return os.path.join(audio_folder, filename)

    filtered_data['full_path'] = filtered_data[file_col].apply(get_full_path)

    filtered_data = (
        df[mask_lat & mask_type & mask_lon]
        .copy()
        .reset_index(drop=True)  #  关键就在这里
    )

    # 打印简报，让你心里有数
    print(f"成功加载！筛选出 {len(filtered_data)} 条符合条件的记录。")

    return filtered_data

# 使用示例
# filtered_df = load_filtered_metadata(r"D:\path\to\csv", r"D:\path\to\audio")