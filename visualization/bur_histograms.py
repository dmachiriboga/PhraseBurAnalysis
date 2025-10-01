import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from utils.data_utils import load_phrasebur_csv, ensure_output_dir, get_artist_from_id

def create_performer_bur_histograms(output_dir="outputs/bur_histograms"):
    """Create BUR histograms for each performer and save as PNG files."""
    # Load the CSV
    df = load_phrasebur_csv()
    
    # Create output directory for histograms
    ensure_output_dir(output_dir)
    
    # Get all unique performers
    performers = df['id'].apply(lambda x: x.split('_')[0]).unique()
    
    # For each performer, collect all BUR values and plot histogram
    for performer in performers:
        # Select all rows for this performer
        performer_rows = df[df['id'].str.startswith(performer)]
        bur_values = performer_rows['swing_ratios'].astype(float)
        if bur_values.empty:
            continue
        # Histogram bins: 0.1 increments from 1.0 to 2.5
        bin_edges = np.arange(1.0, 2.6, 0.1).tolist()
        plt.figure(figsize=(8, 5))
        plt.hist(bur_values, bins=bin_edges, edgecolor='black', alpha=0.7)
        plt.title(f"BUR Histogram for {get_artist_from_id(performer + '_')}")
        plt.xlabel("BUR Value")
        plt.ylabel("Count")
        plt.xticks(bin_edges, rotation=45)
        plt.tight_layout()
        # Save to file
        filename = os.path.join(output_dir, f"{performer}_bur_histogram.png")
        plt.savefig(filename)
        plt.close()
    
    return output_dir

if __name__ == "__main__":
    output_dir = create_performer_bur_histograms()
    print(f"Histograms saved to {output_dir}/ (one PNG per performer)")