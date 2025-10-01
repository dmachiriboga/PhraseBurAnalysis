#!/usr/bin/env python3
"""
BUR Variation Analysis CLI
Analyzes variation (standard deviation) in swing ratio values per phrase.
"""

import pandas as pd
import numpy as np
from collections import defaultdict

from utils.data_utils import load_phrasebur_csv, get_artist_from_id, ensure_output_dir
from analysis.bur_variation_analysis import phrase_variation_stats

def main():
    # Load the CSV
    df = load_phrasebur_csv()

    results = []
    artist_phrase_stds = defaultdict(list)
    total_phrases = 0

    for (solo_id, phrase_id), group in df.groupby(['id', 'seg_id']):
        bur_values = group['swing_ratios'].astype(float).tolist()
        stats = phrase_variation_stats(bur_values)
        if stats is None:
            continue
            
        artist = get_artist_from_id(solo_id)
        artist_phrase_stds[artist].append(stats['std_bur'])
        
        results.append({
            'id': solo_id,
            'seg_id': phrase_id,
            'artist': artist,
            **stats
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

    # Save the phrase-level variation data
    ensure_output_dir()
    variation_df.to_csv("outputs/phrase_bur_variation.csv", index=False)

if __name__ == "__main__":
    main()