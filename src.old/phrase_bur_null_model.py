import numpy as np
import pandas as pd

# Parameters for random data
total_phrases = 4857  # Match your real data
min_phrase_len = 3
max_phrase_len = 20
np.random.seed(42)

# Generate random phrase lengths (matching the distribution in your real data is best, but here we use uniform for demo)
phrase_lengths = np.random.randint(min_phrase_len, max_phrase_len + 1, total_phrases)

# Load observed phrase-level stddevs from real data
# We'll extract stddevs from PhraseBur.csv (semicolon-delimited, columns: id;seg_type;seg_id;swing_ratios)
OBSERVED_MEAN = 1.4137
OBSERVED_STD = 0.5741
obs_phrase_stddevs = []
try:
    df = pd.read_csv('PhraseBur.csv', sep=';')
    # Group by seg_id, calculate stddev for each phrase
    for seg_id, group in df.groupby('seg_id'):
        if len(group['swing_ratios']) > 1:
            obs_phrase_stddevs.append(np.std(group['swing_ratios'].astype(float), ddof=1))
        else:
            obs_phrase_stddevs.append(OBSERVED_STD)  # fallback if only one value
except Exception as e:
    print('Warning: Could not load observed phrase stddevs, using global stddev for all phrases.')
    obs_phrase_stddevs = [OBSERVED_STD] * total_phrases

# Generate random BUR values for each phrase (using observed mean and global stddev)
random_phrases = []
for phrase_id, n in enumerate(phrase_lengths):
    bur_values = np.random.normal(loc=OBSERVED_MEAN, scale=OBSERVED_STD, size=n)
    random_phrases.append(bur_values)

threshold = 0.4# Use the same threshold as your main analysis
n_iterations = 1000
sig_both_list = []
sig_beginning_list = []
sig_end_list = []
sig_none_list = []

for i in range(n_iterations):
    sig_counts = {"sig_both": 0, "sig_beginning": 0, "sig_end": 0, "sig_none": 0}
    for bur_values in random_phrases:
        n = len(bur_values)
        if n < 3:
            continue
        # Shuffle for each iteration to simulate random order
        bur_values_iter = np.random.permutation(bur_values)
        first_bur = bur_values_iter[0]
        last_bur = bur_values_iter[-1]
        middle_bur = bur_values_iter[1:-1]
        mean_middle = np.mean(middle_bur)
        std_middle = np.std(middle_bur, ddof=1) if len(middle_bur) > 1 else 0
        z_first = (first_bur - mean_middle) / std_middle if std_middle > 0 else 0
        z_last = (last_bur - mean_middle) / std_middle if std_middle > 0 else 0
        sig_first = abs(z_first) > 1.96
        sig_last = abs(z_last) > 1.96
        if sig_first and sig_last:
            sig_cat = "sig_both"
        elif sig_first:
            sig_cat = "sig_beginning"
        elif sig_last:
            sig_cat = "sig_end"
        else:
            sig_cat = "sig_none"
        sig_counts[sig_cat] += 1
    sig_total = sum(sig_counts.values())
    sig_both_list.append(100 * sig_counts["sig_both"] / sig_total)
    sig_beginning_list.append(100 * sig_counts["sig_beginning"] / sig_total)
    sig_end_list.append(100 * sig_counts["sig_end"] / sig_total)
    sig_none_list.append(100 * sig_counts["sig_none"] / sig_total)

print("Randomized null model (mean % over 1000 runs, using random BUR values):")
print(f"Both beginning and end statistically significant: {np.mean(sig_both_list):.2f}% ± {np.std(sig_both_list):.2f}%")
print(f"Only beginning statistically significant: {np.mean(sig_beginning_list):.2f}% ± {np.std(sig_beginning_list):.2f}%")
print(f"Only end statistically significant: {np.mean(sig_end_list):.2f}% ± {np.std(sig_end_list):.2f}%")
print(f"Neither statistically significant: {np.mean(sig_none_list):.2f}% ± {np.std(sig_none_list):.2f}%")
