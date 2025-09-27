import pandas as pd
import numpy as np
import os
from collections import defaultdict

# Load the CSV
df = pd.read_csv("PhraseBur.csv", sep=';')

results = []
artist_phrase_counts = defaultdict(int)
artist_highvar_counts = defaultdict(int)

# Helper to format performer names
import re
def get_artist_from_id(id_str):
    artist = id_str.split('_')[0]
    artist = re.sub(r'(?<!^)([A-Z])', r' \1', artist)
    return artist

# Calculate std for each phrase and track per artist
artist_phrase_stds = defaultdict(list)
total_phrases = 0
for (solo_id, phrase_id), group in df.groupby(['id', 'seg_id']):
    bur_values = group['swing_ratios'].astype(float).tolist()
    n = len(bur_values)
    if n < 2:
        continue
    std_bur = np.std(bur_values, ddof=1)
    artist = get_artist_from_id(solo_id)
    artist_phrase_stds[artist].append(std_bur)
    results.append({
        'id': solo_id,
        'seg_id': phrase_id,
        'artist': artist,
        'n_values': n,
        'std_bur': std_bur
    })
    total_phrases += 1

# Convert to DataFrame for easy sorting/analysis
variation_df = pd.DataFrame(results)

# Compute average phrase stddev per artist
artist_avg_std = []
for artist, stds in artist_phrase_stds.items():
    avg_std = np.mean(stds) if stds else 0
    count = len(stds)
    artist_avg_std.append((artist, avg_std, count))

# Sort by average stddev (descending)
artist_avg_std.sort(key=lambda x: x[1], reverse=True)

# Print total phrase average std deviation
if len(variation_df) > 0:
    total_avg_std = variation_df['std_bur'].mean()
    print(f"\nTotal phrase average std deviation: {total_avg_std:.3f}")

# Ask user for number of top performers to display
try:
    n_top = int(input("How many top performers to display? (default 20): ") or 20)
except Exception:
    n_top = 20

print(f"\nTop {n_top} performers:")
for artist, avg_std, count in artist_avg_std[:n_top]:
    print(f"{artist}: avg phrase stddev = {avg_std:.3f} ({count} phrases)")

# Optionally, save the phrase-level variation data
os.makedirs("outputs", exist_ok=True)
variation_df.to_csv("outputs/phrase_bur_variation.csv", index=False)
