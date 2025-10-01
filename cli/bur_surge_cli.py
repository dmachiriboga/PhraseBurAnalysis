#!/usr/bin/env python3
"""
BUR Surge Analysis CLI
Analyzes trends in swing ratio (BUR) values across phrase positions.
"""

import pandas as pd
import numpy as np
import math
from collections import defaultdict
import warnings

from utils.data_utils import load_phrasebur_csv, get_artist_from_id, ensure_output_dir
from analysis.bur_surge_analysis import fit_and_evaluate_models

# Suppress curve fitting warnings
warnings.filterwarnings("ignore")

def main():
    # Load the CSV
    df = load_phrasebur_csv()

    results = []
    artist_phrase_counts = defaultdict(int)
    artist_sig_counts_increase = defaultdict(int)
    artist_sig_counts_decrease = defaultdict(int)

    # Process each phrase
    for (solo_id, phrase_id), group in df.groupby(['id', 'seg_id']):
        bur_values = group['swing_ratios'].astype(float).tolist()
        n = len(bur_values)
        if n < 6:  # Minimum 6 notes for reliable trend detection
            continue

        x = np.arange(n)
        y = np.array(bur_values)

        best_model_name, best_model_data, all_models = fit_and_evaluate_models(x, y)
        artist = get_artist_from_id(solo_id)
        artist_phrase_counts[artist] += 1

        # Check for significant increase/decrease in any model
        counted_increase = False
        counted_decrease = False

        # Linear: p-value < 0.05 AND predicted change >= 0.456 or <= -0.456
        linear = all_models.get('linear')
        if linear and linear['p_value'] is not None and linear['p_value'] < 0.05:
            slope, intercept = linear['params']
            pred_start = slope * x[0] + intercept
            pred_end = slope * x[-1] + intercept
            delta = pred_end - pred_start
            if delta >= 0.456: # TODO: Magic number. where does this come from?
                artist_sig_counts_increase[artist] += 1
                counted_increase = True
            elif delta <= -0.456:
                artist_sig_counts_decrease[artist] += 1
                counted_decrease = True

        # Exponential: R² > 0.8 AND predicted change >= 0.456 or <= -0.456
        exp = all_models.get('exponential')
        if exp and exp['r2'] > 0.8:
            a, b = exp['params']
            pred_start = a * np.exp(b * x[0])
            pred_end = a * np.exp(b * x[-1])
            delta = pred_end - pred_start
            if delta >= 0.456 and not counted_increase:
                artist_sig_counts_increase[artist] += 1
                counted_increase = True
            elif delta <= -0.456 and not counted_decrease:
                artist_sig_counts_decrease[artist] += 1
                counted_decrease = True

        # Logarithmic: R² > 0.8 AND predicted change >= 0.456 or <= -0.456
        logm = all_models.get('logarithmic')
        if logm and logm['r2'] > 0.8:
            a, b = logm['params']
            pred_start = a * np.log(x[0] + 1e-6) + b
            pred_end = a * np.log(x[-1] + 1 + 1e-6) + b  # x[-1]+1 to match fitting
            delta = pred_end - pred_start
            if delta >= 0.456 and not counted_increase:
                artist_sig_counts_increase[artist] += 1
                counted_increase = True
            elif delta <= -0.456 and not counted_decrease:
                artist_sig_counts_decrease[artist] += 1
                counted_decrease = True

        results.append({
            'id': solo_id,
            'seg_id': phrase_id,
            'n_values': n,
            'best_model': best_model_name,
            'best_r2': best_model_data['r2'],
            'artist': artist
        })

    # Overall summary before prompt
    all_total = sum(artist_phrase_counts.values())
    all_inc = sum(artist_sig_counts_increase.values())
    all_dec = sum(artist_sig_counts_decrease.values())
    print(f"\nOverall: {all_inc} / {all_total} phrases with significant increase ({(all_inc/all_total if all_total else 0):.1%})")
    print(f"Overall: {all_dec} / {all_total} phrases with significant decrease ({(all_dec/all_total if all_total else 0):.1%})")

    # Prepare stats for display
    artist_stats_inc = []
    artist_stats_dec = []
    for artist in artist_phrase_counts:
        total = artist_phrase_counts[artist]
        inc = artist_sig_counts_increase[artist]
        dec = artist_sig_counts_decrease[artist]
        pct_inc = inc / total if total else 0
        pct_dec = dec / total if total else 0
        artist_stats_inc.append((artist, total, inc, pct_inc))
        artist_stats_dec.append((artist, total, dec, pct_dec))

    # Sort by total count (descending), then percentage (descending)
    artist_stats_inc.sort(key=lambda x: (x[1], x[3]), reverse=True)
    artist_stats_dec.sort(key=lambda x: (x[1], x[3]), reverse=True)

    # Ask user for number of top performers to display
    try:
        n_top = int(input("How many top performers to display? (default 20): ") or 20)
    except Exception:
        n_top = 20

    print(f"\nTop {n_top} performers (by significant increase):")
    for artist, total, inc, pct_inc in artist_stats_inc[:n_top]:
        print(f"{artist}: {inc} / {total} increase ({pct_inc:.1%})")

    # Print overall percentage for top N increase performers
    if artist_stats_inc[:n_top]:
        total_inc_top = sum(x[2] for x in artist_stats_inc[:n_top])
        total_phrases_top = sum(x[1] for x in artist_stats_inc[:n_top])
        pct_inc_top = total_inc_top / total_phrases_top if total_phrases_top else 0
        print(f"\nTop {n_top} increase performers: {total_inc_top} / {total_phrases_top} = {pct_inc_top:.1%} significant increase")

    print(f"\nTop {n_top} performers (by significant decrease):")
    for artist, total, dec, pct_dec in artist_stats_dec[:n_top]:
        print(f"{artist}: {dec} / {total} decrease ({pct_dec:.1%})")

    # Print overall percentage for top N decrease performers
    if artist_stats_dec[:n_top]:
        total_dec_top = sum(x[2] for x in artist_stats_dec[:n_top])
        total_phrases_top_dec = sum(x[1] for x in artist_stats_dec[:n_top])
        pct_dec_top = total_dec_top / total_phrases_top_dec if total_phrases_top_dec else 0
        print(f"\nTop {n_top} decrease performers: {total_dec_top} / {total_phrases_top_dec} = {pct_dec_top:.1%} significant decrease")

if __name__ == "__main__":
    main()