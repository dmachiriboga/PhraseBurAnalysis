import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the CSV
df = pd.read_csv("PhraseBur.csv", sep=';')

# Create output directory for histograms
output_dir = "bur_histograms"
os.makedirs(output_dir, exist_ok=True)

# Get all unique performers
performers = df['id'].apply(lambda x: x.split('_')[0]).unique()

# Function to insert spaces in performer names (e.g., 'JJohnColtrane' -> 'J John Coltrane')
def format_performer(name):
    import re
    return re.sub(r'(?<!^)([A-Z])', r' \1', name)

# For each performer, collect all BUR values and plot histogram
for performer in performers:
    # Select all rows for this performer
    performer_rows = df[df['id'].str.startswith(performer)]
    bur_values = performer_rows['swing_ratios'].astype(float)
    if bur_values.empty:
        continue
    # Histogram bins: 0.1 increments from 1.0 to 2.5
    bins = np.arange(1.0, 2.6, 0.1)
    plt.figure(figsize=(8, 5))
    plt.hist(bur_values, bins=bins, edgecolor='black', alpha=0.7)
    plt.title(f"BUR Histogram for {format_performer(performer)}")
    plt.xlabel("BUR Value")
    plt.ylabel("Count")
    plt.xticks(bins, rotation=45)
    plt.tight_layout()
    # Save to file
    filename = os.path.join(output_dir, f"{performer}_bur_histogram.png")
    plt.savefig(filename)
    plt.close()

print(f"Histograms saved to {output_dir}/ (one PNG per performer)")
