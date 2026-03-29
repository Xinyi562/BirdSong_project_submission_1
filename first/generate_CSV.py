# Generate a new filtered metadata CSV from metadata_ready
import os

from utils.metadata_ready import metadata_ready





# Get metadata
filtered_df = metadata_ready()


# Save as CSV
filtered_df.to_csv("filtered_metadata_preview.csv", index=False)
print("CSV generated: filtered_metadata_preview.csv")


# confirm file location
print("saved to:", os.getcwd())

