# Used to gain intuitive understanding of the geographic distribution of the recordings.
import pandas as pd
import matplotlib.pyplot as plt

# Reading metadata
df = pd.read_csv(r"/archive/birdsong_metadata.csv")
print(df.columns.tolist())

# Convert latitude and longitute to numeric values
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitute'] = pd.to_numeric(df['longitute'], errors='coerce')


# Remove rows with missing coordinates
print(f"Length before dropping: {len(df)}")
df = df.dropna(subset=["latitude", "longitute"])
print(f"Length after dropping: {len(df)}")


# Filter for 'song' type only.
df = df[df['type'] == 'song']

# Dropping outliers (Using estimation for European continent lat / lon).
df = df[
    ((df["latitude"] >= 35) & (df["latitude"] <= 71)) &
    ((df["longitute"] >= -25) & (df["longitute"] <= 66))
]

# Generate scatter plot.
plt.figure(figsize=(8, 6))
plt.scatter(
    df["longitute"],
    df["latitude"],
    s=25,        # Dot size
    alpha=0.5    # Opacity
)

# Axis & title
plt.xlabel("Longitute")
plt.ylabel("Latitude")
plt.title("Bird Vocalization Locations")

plt.show()