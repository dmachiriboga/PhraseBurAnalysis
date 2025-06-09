import pandas as pd
import numpy as np
from collections import defaultdict
from scipy.stats import linregress

# Load the CSV
df = pd.read_csv("PhraseBur.csv", sep=';')

results = []
artist_phrase_counts = defaultdict(int)
artist_sig_counts_increase = defaultdict(int)
artist_sig_counts_decrease = defaultdict(int)

# Helper to format performer names
import re
def get_artist_from_id(id_str):
    artist = id_str.split('_')[0]
    artist = re.sub(r'(?<!^)([A-Z])', r' \1', artist)
    return artist

for (solo_id, phrase_id), group in df.groupby(['id', 'seg_id']):
    bur_values = group['swing_ratios'].astype(float).tolist()
    n = len(bur_values)
    if n < 3:
        continue
    x = np.arange(n)
    y = np.array(bur_values)
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    sig = p_value < 0.05
    direction = None
    if sig:
        if slope > 0:
            direction = 'increase'
        elif slope < 0:
            direction = 'decrease'
    artist = get_artist_from_id(solo_id)
    artist_phrase_counts[artist] += 1
    if sig and slope > 0:
        artist_sig_counts_increase[artist] += 1
    if sig and slope < 0:
        artist_sig_counts_decrease[artist] += 1
    results.append({
        'id': solo_id,
        'seg_id': phrase_id,
        'n_values': n,
        'slope': slope,
        'p_value': p_value,
        'sig': sig,
        'direction': direction,
        'artist': artist
    })

# Overall summary before prompt
all_total = sum(artist_phrase_counts.values())
all_inc = sum(artist_sig_counts_increase.values())
all_dec = sum(artist_sig_counts_decrease.values())
print(f"\nOverall: {all_inc} / {all_total} phrases with significant increase ({(all_inc/all_total if all_total else 0):.1%})")
print(f"Overall: {all_dec} / {all_total} phrases with significant decrease ({(all_dec/all_total if all_total else 0):.1%})")

# Balanced metric: more weight to percentage, but still rewards phrase count
def balanced_metric(sig_count, total_count):
    if total_count == 0:
        return 0
    pct = sig_count / total_count
    import math
    return pct * (math.log(total_count + 1) ** 1.5)

# Prepare stats for display
artist_stats_inc = []
artist_stats_dec = []
for artist in artist_phrase_counts:
    total = artist_phrase_counts[artist]
    inc = artist_sig_counts_increase[artist]
    dec = artist_sig_counts_decrease[artist]
    pct_inc = inc / total if total else 0
    pct_dec = dec / total if total else 0
    metric_inc = balanced_metric(inc, total)
    metric_dec = balanced_metric(dec, total)
    artist_stats_inc.append((artist, total, inc, pct_inc, metric_inc))
    artist_stats_dec.append((artist, total, dec, pct_dec, metric_dec))

# Sort separately by increase and decrease balanced metric
artist_stats_inc.sort(key=lambda x: x[4], reverse=True)
artist_stats_dec.sort(key=lambda x: x[4], reverse=True)

# Ask user for number of top performers to display
try:
    n_top = int(input("How many top performers to display? (default 20): ") or 20)
except Exception:
    n_top = 20

print(f"\nTop {n_top} performers (by significant increase):")
for artist, total, inc, pct_inc, metric in artist_stats_inc[:n_top]:
    print(f"{artist}: {inc} / {total} increase ({pct_inc:.1%})")

# Print overall percentage for top N increase performers
if artist_stats_inc[:n_top]:
    total_inc_top = sum(x[2] for x in artist_stats_inc[:n_top])
    total_phrases_top = sum(x[1] for x in artist_stats_inc[:n_top])
    pct_inc_top = total_inc_top / total_phrases_top if total_phrases_top else 0
    print(f"\nTop {n_top} increase performers: {total_inc_top} / {total_phrases_top} = {pct_inc_top:.1%} significant increase")

print(f"\nTop {n_top} performers (by significant decrease):")
for artist, total, dec, pct_dec, metric in artist_stats_dec[:n_top]:
    print(f"{artist}: {dec} / {total} decrease ({pct_dec:.1%})")

# Print overall percentage for top N decrease performers
if artist_stats_dec[:n_top]:
    total_dec_top = sum(x[2] for x in artist_stats_dec[:n_top])
    total_phrases_top_dec = sum(x[1] for x in artist_stats_dec[:n_top])
    pct_dec_top = total_dec_top / total_phrases_top_dec if total_phrases_top_dec else 0
    print(f"\nTop {n_top} decrease performers: {total_dec_top} / {total_phrases_top_dec} = {pct_dec_top:.1%} significant decrease")
