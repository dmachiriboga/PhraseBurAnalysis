#!/usr/bin/env python3
"""
BUR Surge Null Model CLI
Tests surge analysis against random data to establish baseline false-positive rates.
"""

import numpy as np
import warnings
from analysis.bur_surge_analysis import fit_and_evaluate_models

# Suppress curve fitting warnings
warnings.filterwarnings("ignore")

def main():
    # Parameters for random data
    total_phrases = 4857  # Match your real data
    min_phrase_len = 6
    max_phrase_len = 20
    np.random.seed(42)

    # Use observed mean and std for BUR values
    OBSERVED_MEAN = 1.41
    OBSERVED_STD = 0.57

    # Generate random phrase lengths
    phrase_lengths = np.random.randint(min_phrase_len, max_phrase_len + 1, total_phrases)

    # Generate random BUR values for each phrase (clipped to 95% observed range)
    BUR_MIN = 0.48
    BUR_MAX = 2.67
    random_phrases = []
    for n in phrase_lengths:
        bur_values = np.random.normal(loc=OBSERVED_MEAN, scale=OBSERVED_STD, size=n)
        bur_values = np.clip(bur_values, BUR_MIN, BUR_MAX)
        random_phrases.append(bur_values)

    # Null model analysis
    sig_inc = 0
    sig_dec = 0
    for bur_values in random_phrases:
        n = len(bur_values)
        if n < 6:
            continue
        x = np.arange(n)
        y = np.array(bur_values)
        best_model_name, best_model_data, all_models = fit_and_evaluate_models(x, y)

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
                sig_inc += 1
                counted_increase = True
            elif delta <= -0.456:
                sig_dec += 1
                counted_decrease = True

        # Exponential: R² > 0.8 AND predicted change >= 0.456 or <= -0.456
        exp = all_models.get('exponential')
        if exp and exp['r2'] > 0.8:
            a, b = exp['params']
            pred_start = a * np.exp(b * x[0])
            pred_end = a * np.exp(b * x[-1])
            delta = pred_end - pred_start
            if delta >= 0.456 and not counted_increase:
                sig_inc += 1
                counted_increase = True
            elif delta <= -0.456 and not counted_decrease:
                sig_dec += 1
                counted_decrease = True

        # Logarithmic: R² > 0.8 AND predicted change >= 0.456 or <= -0.456
        logm = all_models.get('logarithmic')
        if logm and logm['r2'] > 0.8:
            a, b = logm['params']
            pred_start = a * np.log(x[0] + 1e-6) + b
            pred_end = a * np.log(x[-1] + 1 + 1e-6) + b
            delta = pred_end - pred_start
            if delta >= 0.456 and not counted_increase:
                sig_inc += 1
                counted_increase = True
            elif delta <= -0.456 and not counted_decrease:
                sig_dec += 1
                counted_decrease = True

    print(f"\nNULL MODEL (random BUR data):")
    print(f"Significant increase: {sig_inc} / {total_phrases} ({sig_inc/total_phrases:.1%})")
    print(f"Significant decrease: {sig_dec} / {total_phrases} ({sig_dec/total_phrases:.1%})")

if __name__ == "__main__":
    main()