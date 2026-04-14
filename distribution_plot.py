import matplotlib
import librosa
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

from utils.find_project_root import find_project_root






# --- Global Configurations ---
matplotlib.use('Agg') # No window output, increase processing speed

# Audio processing parameters
threshold_db = -30
LAT_COL = "latitude"
SR = 22050 #sr=2frequency,
N_FFT = 2048 #每节车厢有2048个点 (Each compartment has 2048 points.)
HOP_LENGTH = 512 #每次间隔512（第一次：0~2048， 第二次：512~512+2048）(Increase 512 each iteration (first time: 0-2048, second time:512~512+2048))
FIG_COLOR = '#12012C'
CMAP = 'plasma'

# Path Setup
BASE_DIR = find_project_root(__file__, marker="archive")
METADATA_PATH = os.path.join(BASE_DIR, "utils", "filtered_metadata_preview.csv")

if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(f"Metadata not found at {METADATA_PATH}")

filtered_df = pd.read_csv(METADATA_PATH)
OUTPUT_DIR = os.path.join(BASE_DIR, "output_test")
os.makedirs(OUTPUT_DIR, exist_ok=True)
#----------------------------------------------------------------
existing = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("output_") and f.endswith(".png")]
count = len(existing) + 1
out_name = f"output_{count}.png"

# Slice dataframe based on user input
while True:
    user_input = input("Please input percentage（separated by space），total must=100：")
    parts = list(map(int, user_input.split())) #把输入的字符串转化为列表 (Configure input into list type.)
    if sum(parts) == 100:
        break
    else:
        print(f"❌ Invalid total sum of {sum(parts)}. Total must be 100, please re-enter your percentage\n")

cum = np.cumsum([0] + parts) #分组 + 累加 (grouping + accumulating)
n_groups = len(parts) #之前输入几个数字，就是有几组 (number of groups = number of input values)







# --- Data Preparation ---
# Obtain min and max latitude from filtered dataset
lat_min = filtered_df[LAT_COL].min()
lat_max = filtered_df[LAT_COL].max()
# Find latitude boundaries of individual groups
lat_bins = lat_min + (cum / 100) * (lat_max - lat_min)

# Find latitude group for each audio
def lat_to_pct(lat):
    return (lat - lat_min) / (lat_max - lat_min) * 100 #纬度转换为百分数 (Latitude value into latitude percentage)
filtered_df["lat_pct"] = lat_to_pct(filtered_df[LAT_COL])# 新建一列，叫lat_pct (create a new column "lat_pct" in CSV table)

# Prepare blank backgounds based on number of groups
freqs = librosa.fft_frequencies(sr=SR, n_fft=N_FFT) #每个琴键对应的频率 (Find the corresponding frequency of each unit.)
n_freq = len(freqs) #有多少个琴键 (number of units.)
group_sum = {g: np.zeros(n_freq) for g in range(n_groups)} # 有多少group，有多少架钢琴（多少条琴键）(number of groups = number of freq groups)
group_count = {g: 0 for g in range(n_groups)} # Initialize sample counter







# --- Main Processing Loop ---
for idx, row in filtered_df.iterrows():
    try:
        y, sr = librosa.load(row["full_path"], sr=SR) #y:重采样之后的新数据，SR:实际采样率（同一采样率） (y: new data after unifying sample rate, SR: actual sample rate.)
        D = librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH) #声谱图画出来 (draw spectrogram)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max) #振幅转分贝，以最大振幅为标准 (amplitude to db, max amplitude as reference)

        # Data filtering
        mask = S_db >= threshold_db
        cutoff_bin = int(800  * N_FFT / SR) # 找到800Hz对应的琴键 (Cut away sound under 800 Hz)
        mask[:cutoff_bin, :] = False #mask结构：行为频率，列为时间 (mask: row--freq, colum--time)

        # Find occurrence density for each unit based on max occurrence
        count = np.sum(mask, axis=1) #统计每个琴键被按了多少次 (count occurrences of each unit)
        max_count = np.max(count) #找到次数最多的琴键 (find the unit with max occurrence)
        density = count / max_count if max_count > 0 else count


    # Grouping
        p = row["lat_pct"]
        g = None  # 初始化group (Initialize group)

        # Accumulate audio to their according groups
        # 前面所有组：左闭右开 [a , b) (All preceding bins boundaries: left-closed, right-open)
        # 最后一组改成两头都包含 (The last group: closed on both left and right boundary)
        for i in range(n_groups):
            if i == n_groups - 1:
                if cum[i] <= p <= cum[i + 1]:
                    g = i
                    break
            else:
                if cum[i] <= p < cum[i + 1]:
                    g = i
                    break

        if g is None:   # 跳过不落在任何范围内的百分比音频 (Skip audio that cannot be assigned to any latitude group)
            if g is None:
                print(f"Warning: unassigned audio at lat = {row[LAT_COL]:.4f}")
                continue
            continue

        # Print progress
        if group_count[g] == 0:
            print(f"\nProcessing group: {parts[g]}%")
        group_sum[g] += density # 叠加一整个音频 (Accumulate audio spectral features)
        group_count[g] += 1 #该组鸟的数量+1 (number of audios in this group ++)

    except:
        print(f"skip abnormal audio，index{idx}")
        continue

# Prepare final, overall canvas
group_width = 100
# 拼接每组生成黑色画布，高度为1025个频率，宽度为group数量*宽度100
# (Create final blank canvas for concatenation. height: 1025, width: num groups * 100)
total_canvas = np.zeros((n_freq, group_width * n_groups))

for g in range(n_groups):
    # Find left and right pixel boundaries for each group
    x0 = g * group_width
    x1 = (g+1) * group_width

    # Within-group normalization
    sig = group_sum[g]
    peak = np.max(sig)
    if peak > 0:
        sig = sig / peak   # Using the max density of each group for reference
    total_canvas[:, x0:x1] = np.tile(sig.reshape(-1,1), (1, group_width))







# --- Visual Rendering ---
fig_width = max(14, n_groups * 2.6)
plt.figure(figsize=(fig_width, 6), facecolor=FIG_COLOR)
plt.imshow(total_canvas, origin='lower', aspect='auto', cmap=CMAP, #可视化total canvas, 左下角为零坐标 (visualize the total canvas, assign left bottom corner for origin)
           extent=[0, n_groups, freqs[0], freqs[-1]]) #图像左，右，下，上range (range for the x and y axis)

ax = plt.gca() #拎出坐标轴，调整坐标轴(get and adjust the axis）
ax.set_facecolor(FIG_COLOR)
for spine in ax.spines.values():
    spine.set_visible(False)

# Set x and y labels
plt.ylabel('Frequency (Hz)', color='white')
plt.xticks(
    np.arange(n_groups)+0.5,
    [   # x label: degrees, number of audios, percentage
        f"{lat_bins[i]:.2f} deg~\n{lat_bins[i+1]:.2f} deg\n(n={group_count[i]})\n{parts[i]}%"
        for i in range(n_groups)
    ],
    color='white',
    fontsize = max(5.5, 9.5 - n_groups*0.35)
)
plt.tick_params(axis='y', colors='white')
plt.title('Frequency Overlay graph', color='white')






# --- Save and show output ---
plt.savefig(os.path.join(OUTPUT_DIR, out_name),
            facecolor=FIG_COLOR, bbox_inches='tight', dpi=150)
plt.close()

print("\nFinished processing!")
total_valid = sum(group_count.values())
print(f"Number of valid birdsongs:{total_valid}")
