import numpy as np
import pandas as pd
from collections import defaultdict
from scipy.stats import linregress
from scipy.optimize import curve_fit
import re
import warnings

# Parameters for random data
total_phrases = 4857  # Match your real data
min_phrase_len = 3
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

# Model functions
def exp_func(t, a, b):
    return a * np.exp(b * t)

def log_func(t, a, b):
    return a * np.log(t + 1e-6) + b

def fit_and_evaluate_models(x, y):
    models = {}

    # Linear
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
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
        popt, _ = curve_fit(log_func, x + 1, y, maxfev=10000)
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

# Suppress curve fitting warnings
warnings.filterwarnings("ignore")

# Null model analysis
sig_inc = 0
sig_dec = 0
for bur_values in random_phrases:
    n = len(bur_values)
    if n < 3:
        continue
    x = np.arange(n)
    y = np.array(bur_values)
    best_model_name, best_model_data, all_models = fit_and_evaluate_models(x, y)

    counted_increase = False
    counted_decrease = False

    # Linear: p-value < 0.05
    linear = all_models.get('linear')
    if linear and linear['p_value'] is not None and linear['p_value'] < 0.05:
        if linear['direction'] == 'increase':
            sig_inc += 1
            counted_increase = True
        elif linear['direction'] == 'decrease':
            sig_dec += 1
            counted_decrease = True

    # Exponential: R² > 0.5
    exp = all_models.get('exponential')
    if exp and exp['r2'] > 0.5:
        if exp['direction'] == 'increase' and not counted_increase:
            sig_inc += 1
            counted_increase = True
        elif exp['direction'] == 'decrease' and not counted_decrease:
            sig_dec += 1
            counted_decrease = True

    # Logarithmic: R² > 0.5
    logm = all_models.get('logarithmic')
    if logm and logm['r2'] > 0.5:
        if logm['direction'] == 'increase' and not counted_increase:
            sig_inc += 1
            counted_increase = True
        elif logm['direction'] == 'decrease' and not counted_decrease:
            sig_dec += 1
            counted_decrease = True

print(f"\nNULL MODEL (random BUR data):")
print(f"Significant increase: {sig_inc} / {total_phrases} ({sig_inc/total_phrases:.1%})")
print(f"Significant decrease: {sig_dec} / {total_phrases} ({sig_dec/total_phrases:.1%})")