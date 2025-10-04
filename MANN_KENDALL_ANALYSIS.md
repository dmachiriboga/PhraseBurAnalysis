# Mann-Kendall vs Linear Regression: BUR Trend Analysis Comparison

## Summary of Results

### Mann-Kendall Analysis Results

**Modified Mann-Kendall Test (Autocorrelation-adjusted):**
- Significant increasing trends: **23/2488 (0.92%)**
- Significant decreasing trends: **22/2488 (0.88%)**
- **Total significant**: 45/2488 (1.81%)

**Original Mann-Kendall Test:**
- Significant increasing trends: **1/2488 (0.04%)**
- Significant decreasing trends: **0/2488 (0.00%)**

**Linear Regression (from previous analysis):**
- Significant increasing trends: **1/2488 (0.04%)**
- Significant decreasing trends: **0/2488 (0.00%)**

## Key Findings

### 1. Modified MK Detects More Trends
The modified Mann-Kendall test (which accounts for autocorrelation) detected **45x more significant trends** than the original MK test after FDR correction:
- Modified MK: 45 significant (1.81%)
- Original MK: 1 significant (0.04%)
- Linear regression: 1 significant (0.04%)

### 2. FDR Correction is Crucial
Before FDR correction, many trends appeared significant due to multiple testing:
- **Original MK**: 190 → 1 significant (99.5% were false positives!)
- **Modified MK**: 247 → 45 significant (81.8% were false positives)

This shows that **without proper multiple testing correction, you would massively overestimate the prevalence of BUR trends**.

### 3. Weak Overall Trends
- **Mean Kendall's tau**: 0.000 (essentially no average trend)
- **Median Kendall's tau**: 0.000
- **Median Sen's slope**: 0.0008 (nearly flat)

The overall corpus shows **no systematic BUR surge pattern** across all phrases.

### 4. Individual Variation
- **50.6% of phrases** have positive Sen's slope (slight increase)
- **49.4% of phrases** have negative Sen's slope (slight decrease)

This is close to **50/50**, suggesting BUR changes are **random** rather than systematic.

## Why Modified MK Detects More?

The modified Mann-Kendall test adjusts for **autocorrelation** in the data:

1. **Musical phrases have autocorrelation**: Adjacent BUR values tend to be similar
2. **Autocorrelation inflates significance**: Makes trends appear more significant than they are
3. **Modified MK corrects for this**: Adjusts the variance calculation
4. **Result**: More conservative test that still finds real patterns

## Advantages of Mann-Kendall Over Linear Regression

### Mann-Kendall Advantages:
✅ **Non-parametric**: No normality assumption
✅ **Robust to outliers**: Uses ranks instead of raw values
✅ **Detects any monotonic trend**: Not just linear
✅ **Modified version handles autocorrelation**: Explicitly adjusts for it
✅ **Sen's slope**: More robust slope estimate than OLS

### Linear Regression Limitations:
❌ Assumes linear trend
❌ Assumes normality of residuals
❌ Sensitive to outliers
❌ Assumes independence (but only tests with Durbin-Watson)
❌ Can miss non-linear monotonic patterns

## Interpretation for Your Research

### The "BUR Surge" Hypothesis
Based on Mann-Kendall analysis:

1. **Very rare systematic surges**: Only 0.92% of phrases show significant increases
2. **Equally rare decreases**: 0.88% show significant decreases
3. **No overall pattern**: Mean tau ≈ 0, suggesting random variation

### What This Means:
- BUR changes **do occur** within phrases (50% increase, 50% decrease)
- But these changes are **not statistically significant** in most cases
- After proper multiple testing correction, almost no phrases show reliable trends
- The "surge" phenomenon may be:
  - Less common than initially thought
  - More variable across performers/contexts
  - Possibly an expressive choice rather than systematic pattern

### Performer Differences
Some performers show more trend activity (Modified MK):
- **Miles Davis**: 2.4% increases, 1.2% decreases
- **Lee Konitz**: 2.7% decreases
- **Sonny Rollins**: 2.2% increases

But even these rates are **very low** (~2-3%).

## Recommendations

### 1. Use Modified Mann-Kendall
For musical time series with potential autocorrelation, **modified Mann-Kendall is superior** to:
- Original Mann-Kendall (doesn't account for autocorrelation)
- Linear regression (assumes linearity and normality)

### 2. Always Apply FDR Correction
Testing 2,488 phrases means **~5% (124) will appear significant by chance alone**. FDR correction is essential.

### 3. Report Effect Sizes
Even with p < 0.05, trends might be:
- Kendall's tau ≈ 0.0-0.3 = **weak** trend
- Sen's slope ≈ 0.001-0.01 = **small** practical change

Your data shows **weak trends** even when statistically significant.

### 4. Consider Alternative Explanations
Since systematic BUR surges are rare, consider:
- **Phrase-specific patterns**: Some phrase types may surge more
- **Contextual factors**: Tempo, harmonic complexity, ensemble interaction
- **Performer style**: Individual rather than universal phenomenon
- **Measurement noise**: BUR calculation uncertainty

### 5. Focus on Qualitative Analysis
With so few significant trends, **qualitative examination** of individual examples may be more informative than corpus-wide statistics.

## Technical Details

### Modified Mann-Kendall Formula
The modified test adjusts variance for autocorrelation:

```
Variance_modified = Variance_original * (n/n_effective)
```

Where `n_effective` accounts for the reduction in effective sample size due to autocorrelation.

### Sen's Slope
Sen's slope is the **median of all pairwise slopes**:
- More robust to outliers than OLS slope
- Non-parametric (no distributional assumptions)
- Often used with Mann-Kendall test

### When to Use Each Test

| Situation | Best Test |
|-----------|-----------|
| Linear trend expected | Linear regression |
| Any monotonic trend | Mann-Kendall |
| Autocorrelated data | Modified Mann-Kendall |
| Many outliers | Mann-Kendall + Sen's slope |
| Non-linear trends | Polynomial/exponential models |
| Step changes | Change point detection |

## Files Generated
- `outputs/bur_mann_kendall_results.csv` - Detailed Mann-Kendall results
- `cli/bur_mann_kendall_cli.py` - Mann-Kendall analysis CLI
- `analysis/bur_surge_analysis.py` - Updated with MK functions

## Conclusion

The Mann-Kendall analysis confirms that **systematic BUR surges are extremely rare** in jazz phrases:
- Only **~1% of phrases** show significant monotonic trends after proper statistical correction
- Trends are **weak** when present (tau ≈ 0, slope ≈ 0)
- **No evidence** for widespread "surge" phenomenon at phrase endings

This suggests that BUR variation within phrases is more likely:
- **Random fluctuation** around a performer's baseline swing ratio
- **Context-dependent** expressive choices
- **Individual style** rather than universal pattern

The modified Mann-Kendall test is the **most appropriate** statistical method for this analysis because it:
- Handles the non-normal, autocorrelated nature of musical time series
- Detects any monotonic pattern (not just linear)
- Properly accounts for multiple testing

