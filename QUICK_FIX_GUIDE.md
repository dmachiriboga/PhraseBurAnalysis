# Quick Fix Guide - What to Do Now

## **TL;DR - The Problem**

Your **25% localized surge rate is wrong**. It's likely only ~2-3% after proper correction.

You tested **~100,000 windows** but only corrected for **2,488 tests**. This is like:
- Playing the lottery 100,000 times
- But only correcting your odds for 2,488 plays
- Result: massive false positives

---

## **What Was Fixed Already** ✓

1. ✅ One-tailed test bug (was giving wrong p-values for decreases)
2. ✅ Sen's slope confidence interval (was using wrong formula)
3. ✅ Added warnings in code docstrings explaining all issues

---

## **What You Need to Fix** ⚠️

### **Priority 1: Localized Surge Analysis (CRITICAL)**

**File:** `cli/bur_localized_surge_cli.py`

**Current (WRONG):**
```python
# Line ~85-95
p_values_window = results_df['strongest_p_value'].dropna().tolist()  # Only 2,488 p-values
reject, p_corrected = fdr_correction(p_values_window, alpha=FDR_ALPHA)
```

**Fix Option A - Proper Correction (RECOMMENDED):**
```python
# Collect ALL p-values from ALL windows
all_window_p_values = []
all_window_info = []

for (solo_id, seg_id), group in grouped:
    bur_values = group['swing_ratios'].tolist()
    result = sliding_window_surge_analysis_seasonal(bur_values, ...)
    
    if result and result['surges']:
        for surge in result['surges']:
            all_window_p_values.append(surge['p_value'])
            all_window_info.append({
                'id': solo_id,
                'seg_id': seg_id,
                'window_start': surge['start_pos'],
                'window_size': surge['window_size'],
                'p_value': surge['p_value'],
                'tau': surge['tau'],
                # ... other info
            })

# Apply FDR to ALL ~100,000 p-values
reject, p_corrected = fdr_correction(all_window_p_values, alpha=FDR_ALPHA)

# Add corrected p-values back
for i, info in enumerate(all_window_info):
    info['p_corrected'] = p_corrected[i]
    info['significant'] = reject[i]

# Count how many are still significant
n_significant = sum(reject)
print(f"Significant windows after proper FDR: {n_significant} / {len(all_window_p_values)}")
```

**Fix Option B - Non-Overlapping Windows (SIMPLER):**
```python
# In bur_surge_analysis.py, modify sliding_window_surge_analysis_seasonal:

# Change:
for start in range(n - win_size + 1):  # Overlapping

# To:
for start in range(0, n - win_size + 1, win_size):  # Non-overlapping (step = window size)
```

This reduces tests from ~40 per phrase to ~2-3 per phrase, making FDR correction more appropriate.

---

### **Priority 2: Step Change Detection**

**File:** `analysis/bur_surge_analysis.py`, function `step_change_analysis()`

**Option A - Use Proper Changepoint Detection:**
```python
# Install ruptures package
# pip install ruptures

import ruptures as rpt

def step_change_analysis_fixed(bur_values, min_step_size=0.1):
    n = len(bur_values)
    if n < MIN_BUR_VALUES:
        return None
    
    y = np.array(bur_values, dtype=float)
    
    # Use PELT algorithm for changepoint detection
    algo = rpt.Pelt(model="rbf").fit(y)
    result = algo.predict(pen=10)  # Penalty parameter controls number of changepoints
    
    if len(result) > 1:  # Found at least one changepoint
        # result contains changepoint positions
        # This method accounts for multiple testing
        # ... process results
```

**Option B - Add Bonferroni Correction:**
```python
# After finding best_p_value:
n_splits_tested = n - 5  # Number of splits actually tested

# Apply Bonferroni correction
p_value_corrected = min(1.0, best_p_value * n_splits_tested)

return {
    'has_step': p_value_corrected < 0.05,
    'p_value': best_p_value,
    'p_value_corrected': p_value_corrected,  # Add this
    # ... rest
}
```

---

### **Priority 3: Test for Periodicity**

Before using `period=4`, verify it exists:

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def test_for_periodicity(bur_values, max_period=8):
    """Test if BUR values have periodic structure."""
    y = np.array(bur_values, dtype=float)
    
    # Method 1: Autocorrelation function
    acf = np.correlate(y - y.mean(), y - y.mean(), mode='full')
    acf = acf[len(acf)//2:]
    acf = acf / acf[0]
    
    # Look for peaks in ACF at lag=4
    if len(acf) > 4:
        lag4_acf = acf[4]
        print(f"ACF at lag 4: {lag4_acf:.3f}")
        
        # If ACF(4) > 0.3, suggests period=4 structure
        has_period_4 = lag4_acf > 0.3
    else:
        has_period_4 = False
    
    # Method 2: Spectral analysis (periodogram)
    if len(y) > 10:
        frequencies, power = signal.periodogram(y)
        # Look for peak at frequency = 1/4
        # ... (more complex)
    
    return has_period_4

# Test on your data:
n_phrases_with_period4 = 0
for phrase in phrases:
    if test_for_periodicity(phrase):
        n_phrases_with_period4 += 1

print(f"Phrases with period=4 structure: {n_phrases_with_period4} / {total_phrases}")
```

**If <30% of phrases show period=4, DON'T USE SEASONAL TESTS.**

---

## **Expected Results After Fixes**

| Analysis | Before | After Proper Correction |
|----------|--------|------------------------|
| Localized surges | 25.36% | ~2-3% (est.) |
| Step changes | 4.30% | ~2-3% (est.) |
| Full-phrase MK | 1.81% | 1.81% (already correct) |

Your corrected conclusion will be:
> "Systematic BUR surges are rare (~2%) regardless of analysis method (full-phrase, localized, or step change). BUR variation within phrases appears largely random."

---

## **Testing Your Fixes**

### **1. Sanity Check:**
```python
# After implementing fixes, run:
print(f"Total windows tested: {total_windows}")
print(f"P-values collected: {len(all_p_values)}")
print(f"Should be equal: {total_windows == len(all_p_values)}")
```

### **2. Compare to Random Data:**
```python
# Generate random data with NO trends
import numpy as np

random_results = []
for _ in range(2488):
    fake_phrase = np.random.normal(1.4, 0.2, 12)  # Random BUR values
    result = sliding_window_analysis_fixed(fake_phrase)
    random_results.append(result)

# Count significant in random data
random_sig = sum(1 for r in random_results if r['significant'])
print(f"Significant in random data: {random_sig} / 2488")
print(f"Expected at α=0.05: ~124 (5%)")
print(f"If you see >>124, your correction is still too lenient")
```

### **3. Compare Methods:**
```python
# All methods should give similar rates if they're working correctly:
methods = {
    'Full-phrase MK': full_phrase_rate,
    'Localized (fixed)': localized_rate_fixed,
    'Step change (fixed)': step_change_rate_fixed
}

for method, rate in methods.items():
    print(f"{method}: {rate:.2%}")

# Should all be ~1-3%
```

---

## **Timeline**

- **Today:** Read this guide, understand the issues
- **Tomorrow:** Implement Fix Option B (non-overlapping windows) - EASIEST
- **This week:** Test results, compare to random data
- **Next week:** Implement proper changepoint detection (if needed)
- **Update manuscript:** Reframe findings based on corrected results

---

## **Don't Panic** 🎯

- Your full-phrase analyses are **solid**
- Finding ~2% significant is actually **more interesting** scientifically
- Shows you're doing statistics correctly (rare in music research!)
- Rare patterns are more meaningful than common ones
- This makes your research **more credible**, not less

---

## **Questions to Ask Yourself**

1. ✅ Did I collect ALL p-values for FDR correction?
2. ✅ Do my windows overlap? (If yes, consider non-overlapping)
3. ✅ Did I correct for testing multiple split points?
4. ✅ Did I verify the period=4 assumption?
5. ✅ Do my results make sense on random data?

---

## **Getting Help**

If you need help implementing these fixes:
1. Start with the SIMPLER fixes (Option B - non-overlapping windows)
2. Test on a small subset of data first
3. Compare results to original to see the difference
4. Consult with a statistician if needed

The hardest part is done - **you identified the problems**. Now just fix them systematically.

**Good luck!** 🚀
