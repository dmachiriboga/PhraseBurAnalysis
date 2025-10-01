import numpy as np
from scipy.stats import linregress
from scipy.optimize import curve_fit

def exp_func(t, a, b):
    return a * np.exp(b * t)

def log_func(t, a, b):
    return a * np.log(t + 1e-6) + b # 1e-6 is a tiny number to avoid log(0)

def fit_and_evaluate_models(x, y):
    models = {}
    # Linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, y)  # type: ignore[misc]
    models['linear'] = {
        'params': (slope, intercept),
        'r2': r_value ** 2,  # type: ignore[operator]
        'p_value': p_value,
        'direction': 'increase' if slope > 0 else ('decrease' if slope < 0 else None)  # type: ignore[operator]
    }
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
    best_model = max(models.items(), key=lambda x: x[1]['r2'])
    return best_model[0], best_model[1], models
