import pandas as pd
import numpy as np
from collections import defaultdict
from scipy.stats import linregress
from scipy.optimize import curve_fit
import re
import warnings

# Load the CSV
df = pd.read_csv("PhraseBur.csv", sep=';')

results = []
artist_phrase_counts = defaultdict(int)
artist_sig_counts_increase = defaultdict(int)
artist_sig_counts_decrease = defaultdict(int)

# Helper to format performer names
def get_artist_from_id(id_str):
    artist = id_str.split('_')[0]
    artist = re.sub(r'(?<!^)([A-Z])', r' \1', artist)
    return artist

# Suppress curve fitting warnings
warnings.filterwarnings("ignore")

# Model functions
def exp_func(t, a, b):
    return a * np.exp(b * t)

def log_func(t, a, b):
    # Add small value to avoid log(0)
    return a * np.log(t + 1e-6) + b

def fit_and_evaluate_models(x, y):
    models = {}

    # Linear
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    y_pred = slope * x + intercept
    models['linear'] = {
        'params': (slope, intercept),
        'r2': r_value ** 2,
        'p_value': p_value,
        'direction': 'increase' if slope > 0 else ('decrease' if slope < 0 else None)
    }

    # Exponential
    try:
        popt, _ = curve_fit(exp_func, x, y, maxfev=10000)
        y_exp = exp_func(x, *popt)
        r2_exp = 1 - np.sum((y - y_exp) ** 2) / np.sum((y - np.mean(y)) ** 2)
        direction = 'increase' if popt[1] > 0 else ('decrease' if popt[1] < 0 else None)
        models['exponential'] = {
            'params': popt,
            'r2': r2_exp,
            'p_value': None,
            'direction': direction
        }
    except Exception:
        pass

    # Logarithmic
    try:
        popt, _ = curve_fit(log_func, x + 1, y, maxfev=10000)  # x+1 to avoid log(0)
        y_log = log_func(x + 1, *popt)
        r2_log = 1 - np.sum((y - y_log) ** 2) / np.sum((y - np.mean(y)) ** 2)
        direction = 'increase' if popt[0] > 0 else ('decrease' if popt[0] < 0 else None)
        models['logarithmic'] = {
            'params': popt,
            'r2': r2_log,
            'p_value': None,
            'direction': direction
        }
    except Exception:
        pass

    # Find best model by R²
    best_model = max(models.items(), key=lambda x: x[1]['r2'])
    return best_model[0], best_model[1], models

# Process each phrase
for (solo_id, phrase_id), group in df.groupby(['id', 'seg_id']):
    bur_values = group['swing_ratios'].astype(float).tolist()
    n = len(bur_values)
    if n < 3:
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
        if delta >= 0.456:
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