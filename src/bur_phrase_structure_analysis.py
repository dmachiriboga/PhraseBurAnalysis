import pandas as pd
import numpy as np
from collections import defaultdict

# Load the CSV
df = pd.read_csv("PhraseBur.csv", sep=';')

# Set the minimum absolute increase in bur required for 'higher' (e.g., 0.4 means first/last must be at least 0.4 higher than mean_middle)
threshold = 0.4 # Change this value as needed

# Option to toggle between 'sig_both' only or all statistically significant phrases (sig_first or sig_last or both)
# Set this variable to 'both' or 'any'
sig_mode = 'any'  # options: 'both', 'any'

results = []
category_counts = {"both_higher": 0, "beginning_higher": 0, "end_higher": 0, "none_higher": 0}
sig_counts = {"sig_both": 0, "sig_beginning": 0, "sig_end": 0, "sig_none": 0}
total = 0

artist_phrase_counts = defaultdict(int)
artist_sig_counts = defaultdict(int)

def get_artist_from_id(id_str):
    # Assumes format Performer_Song_FINAL
    import re
    artist = id_str.split('_')[0]
    # Insert space before each capital letter (except the first)
    artist = re.sub(r'(?<!^)([A-Z])', r' \1', artist)
    return artist

for (solo_id, phrase_id), group in df.groupby(['id', 'seg_id']):
    bur_values = group['swing_ratios'].astype(float).tolist()
    n = len(bur_values)
    if n < 3:
        continue
    first_bur = bur_values[0]
    last_bur = bur_values[-1]
    middle_bur = bur_values[1:-1]
    mean_middle = np.mean(middle_bur)
    std_middle = np.std(middle_bur, ddof=1) if len(middle_bur) > 1 else 0
    first_higher = (first_bur - mean_middle) > threshold
    last_higher = (last_bur - mean_middle) > threshold

    # Statistical significance (z-score, two-tailed, p<0.05 => |z|>1.96)
    z_first = (first_bur - mean_middle) / std_middle if std_middle > 0 else 0
    z_last = (last_bur - mean_middle) / std_middle if std_middle > 0 else 0
    sig_first = abs(z_first) > 1.96
    sig_last = abs(z_last) > 1.96

    if first_higher and last_higher:
        category = "both_higher"
    elif first_higher:
        category = "beginning_higher"
    elif last_higher:
        category = "end_higher"
    else:
        category = "none_higher"

    # Statistically significant categories
    if sig_first and sig_last:
        sig_cat = "sig_both"
    elif sig_first:
        sig_cat = "sig_beginning"
    elif sig_last:
        sig_cat = "sig_end"
    else:
        sig_cat = "sig_none"
    sig_counts[sig_cat] += 1

    category_counts[category] += 1
    total += 1

    # Track artist stats
    artist = get_artist_from_id(solo_id)
    artist_phrase_counts[artist] += 1
    if sig_first or sig_last:
        artist_sig_counts[artist] += 1

    results.append({
        "id": solo_id,
        "seg_id": phrase_id,
        "first_bur": first_bur,
        "last_bur": last_bur,
        "mean_middle_bur": mean_middle,
        "first_vs_middle": "higher" if first_higher else "lower",
        "last_vs_middle": "higher" if last_higher else "lower",
        "category": category,
        "n_values": n,
        "z_first": z_first,
        "z_last": z_last,
        "sig_first": sig_first,
        "sig_last": sig_last,
        "sig_category": sig_cat
    })

# Convert to DataFrame and save
out = pd.DataFrame(results)
out.to_csv("phrase_bur_evolution.csv", index=False)

# Calculate percentages (excluding "both_higher" from beginning/end percentages)
pct_both = 100 * category_counts["both_higher"] / total if total else 0
pct_beginning = 100 * category_counts["beginning_higher"] / total if total else 0
pct_end = 100 * category_counts["end_higher"] / total if total else 0
pct_none = 100 * category_counts["none_higher"] / total if total else 0

print(f"Total phrases analyzed: {total}")
print(f'Both beginning and end higher: {pct_both:.1f}%')
print(f'Only beginning higher: {pct_beginning:.1f}%')
print(f'Only end higher: {pct_end:.1f}%')
print(f'Neither higher: {pct_none:.1f}%')

# For reporting, exclude "both_higher" from beginning/end percentages
pct_beginning_only = 100 * category_counts["beginning_higher"] / total if total else 0
pct_end_only = 100 * category_counts["end_higher"] / total if total else 0

print("\nSummary (excluding 'both_higher' from beginning/end):")
print(f"Percentage of phrases where only the beginning is higher: {pct_beginning_only:.1f}%")
print(f"Percentage of phrases where only the end is higher: {pct_end_only:.1f}%")
print(f"Percentage of phrases where both are higher: {pct_both:.1f}%")
print(f"Percentage of phrases where neither is higher: {pct_none:.1f}%")

# Statistical significance summary
sig_total = sum(sig_counts.values())
pct_sig_both = 100 * sig_counts["sig_both"] / sig_total if sig_total else 0
pct_sig_beginning = 100 * sig_counts["sig_beginning"] / sig_total if sig_total else 0
pct_sig_end = 100 * sig_counts["sig_end"] / sig_total if sig_total else 0
pct_sig_none = 100 * sig_counts["sig_none"] / sig_total if sig_total else 0

print("\nStatistical significance summary (p < 0.05, |z| > 1.96):")
print(f"Both beginning and end statistically significant: {pct_sig_both:.1f}%")
print(f"Only beginning statistically significant: {pct_sig_beginning:.1f}%")
print(f"Only end statistically significant: {pct_sig_end:.1f}%")
print(f"Neither statistically significant: {pct_sig_none:.1f}%")

# After all calculations, print top 20 performers by a new metric emphasizing phrase count
# Only count 'both' statistically significant phrases for the breakdown

def emphasized_metric(sig_count, total_count):
    if total_count == 0:
        return 0
    pct = sig_count / total_count
    import math
    log_n = math.log(total_count + 1)
    return pct * (log_n ** 2)

# Prompt user for number of top performers to display
try:
    n_top = int(input("How many top performers to display? (default 20): ") or 20)
except Exception:
    n_top = 20

# Count only 'sig_both' or any statistically significant phrases for each artist
artist_sig_counts_toggle = defaultdict(int)
for r in results:
    if sig_mode == 'both':
        if r['sig_category'] == 'sig_both':
            artist = get_artist_from_id(r['id'])
            artist_sig_counts_toggle[artist] += 1
    elif sig_mode == 'any':
        if r['sig_first'] or r['sig_last']:
            artist = get_artist_from_id(r['id'])
            artist_sig_counts_toggle[artist] += 1

artist_stats = [
    (artist, artist_phrase_counts[artist], artist_sig_counts_toggle[artist], artist_sig_counts_toggle[artist] / artist_phrase_counts[artist] if artist_phrase_counts[artist] > 0 else 0, emphasized_metric(artist_sig_counts_toggle[artist], artist_phrase_counts[artist]))
    for artist in artist_phrase_counts
]
artist_stats.sort(key=lambda x: x[4], reverse=True)

if sig_mode == 'both':
    print(f"\nTop {n_top} performers (artist, total phrases, both statistically significant phrases, percentage):")
else:
    print(f"\nTop {n_top} performers (artist, total phrases, any statistically significant phrases, percentage):")
for artist, total_phrases, sig_phrases, pct, _ in artist_stats[:n_top]:
    if sig_mode == 'both':
        print(f"{artist}: {sig_phrases} / {total_phrases} both statistically significant phrases ({pct:.1%})")
    else:
        print(f"{artist}: {sig_phrases} / {total_phrases} any statistically significant phrases ({pct:.1%})")

# Calculate and print the overall ratio for the top N performers, only for selected statistically significant phrases

top_n = artist_stats[:n_top]
total_sig = 0
total_phrases = 0
for artist, total_phrases_artist, sig_phrases_artist, pct, _ in top_n:
    total_sig += sig_phrases_artist
    total_phrases += total_phrases_artist

ratio = total_sig / total_phrases if total_phrases else 0
if sig_mode == 'both':
    print(f"\nTop {n_top} performers (both statistically significant): {total_sig} / {total_phrases} = {ratio:.3%}")
else:
    print(f"\nTop {n_top} performers (any statistically significant): {total_sig} / {total_phrases} = {ratio:.3%}")
