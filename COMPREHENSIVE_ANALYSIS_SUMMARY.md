# Comprehensive BUR Surge Analysis - Summary

## Overview
This document summarizes the results of comprehensive BUR (Beat-Upbeat Ratio) trend analysis using multiple statistical models to detect different types of swing timing patterns in jazz phrases.

## Models Implemented

### 1. **Linear Trend Analysis**
- **Model**: y = mx + b
- **Detects**: Steady, constant increases or decreases in BUR
- **Statistical test**: Linear regression with t-test on slope
- **Results**: 1/2488 phrases (0.04%) show significant linear increase

### 2. **Exponential Trend Analysis**
- **Model**: y = a * exp(b * x)
- **Detects**: Accelerating increases (slow start, rapid increase at end)
- **Statistical test**: Log-linear regression
- **Results**: 1/2488 phrases (0.04%) show significant exponential pattern
- **Use case**: Captures "building momentum" timing patterns

### 3. **Logarithmic Trend Analysis**
- **Model**: y = a + b * ln(x + 1)
- **Detects**: Rapid initial changes that level off
- **Statistical test**: Linear regression on log-transformed x-values
- **Results**: 0/2488 phrases (0.00%) show significant logarithmic pattern
- **Use case**: Captures "initial burst" timing patterns

### 4. **Quadratic Trend Analysis**
- **Model**: y = a + bx + cx²
- **Detects**: U-shaped or inverted-U curved patterns
- **Statistical test**: F-test comparing quadratic vs linear fit
- **Results**: 1/2488 phrases (0.04%) show significant quadratic pattern
- **Use case**: Captures "swell" or "dip" timing patterns

### 5. **Step Change Detection**
- **Method**: Sliding window comparison of phrase segments
- **Detects**: Sudden jumps in BUR at specific points
- **Statistical test**: Welch's t-test comparing segments before/after split
- **Results**: 107/2488 phrases (4.30%) show significant step changes
  - Upward steps: 284 detected (before FDR correction)
  - Downward steps: 263 detected (before FDR correction)
- **Use case**: Captures abrupt timing shifts within phrases

### 6. **End-Phrase Surge Detection**
- **Method**: Compare last 25% of phrase to rest
- **Detects**: Specific pattern of timing increase at phrase endings
- **Statistical test**: One-tailed t-test with Cohen's d effect size
- **Results**: 142/2488 phrases (0.08%) show significant end surges
- **Use case**: Tests the specific "BUR surge" hypothesis mentioned in paper

## Key Findings

### Model Fit Quality (R² comparison)
- **Quadratic models fit best**: 87.6% of phrases
- **Logarithmic models**: 12.4% of phrases
- **Exponential models**: 0.04% of phrases
- **Linear models**: Not best fit for any phrase

This suggests that BUR patterns are predominantly **curved** (quadratic) rather than linear.

### Statistical Significance After FDR Correction
Despite good model fits, very few phrases show statistically significant trends after multiple testing correction:

- **Linear**: 0.04% significant
- **Exponential**: 0.04% significant
- **Logarithmic**: 0.00% significant
- **Quadratic**: 0.04% significant
- **Step changes**: 4.30% detected
- **End surges**: 0.08% detected

### Performer Variation
Some performers show more timing variation patterns:

**Highest Step Change Rates:**
- Stan Getz: 38.7%
- Phil Woods: 31.9%
- David Liebman: 31.0%
- Michael Brecker: 30.1%

**Highest End-Surge Rates:**
- Phil Woods: 10.1%
- Stan Getz: 9.7%
- Lee Konitz: 8.0%
- Sonny Rollins: 7.6%

**Lowest Variation:**
- Ornette Coleman: 12.9% step changes, 3.2% end surges

## Interpretation

### Why So Few Significant Results?
1. **Multiple testing correction is stringent**: Testing 2,488 phrases requires strong correction
2. **Within-phrase variation is high**: Individual differences may exceed systematic patterns
3. **Phrase length matters**: Shorter phrases have fewer data points for trend detection
4. **Autocorrelation**: Adjacent BUR values may be correlated, reducing statistical power

### What Does This Mean for the "BUR Surge" Hypothesis?
The original hypothesis that BUR increases toward phrase endings is:
- **Not strongly supported** by linear or exponential trend analysis
- **Moderately supported** by step change detection (4.3% of phrases)
- **Weakly supported** by end-surge detection (0.08% after correction)

However:
- The **qualitative pattern may still exist** but be less systematic than initially thought
- **Individual performer differences** are substantial
- **Different surge types** (steps vs gradual increases) may have different frequencies

### Best Practices Going Forward

1. **Use quadratic models** as baseline (best fit for most phrases)
2. **Report both uncorrected and FDR-corrected results**
3. **Focus on effect sizes** in addition to p-values
4. **Examine performer-level patterns** rather than corpus-wide trends
5. **Consider phrase length** as a confounding variable
6. **Visualize individual phrases** to understand pattern diversity

## Files Generated

- `outputs/bur_comprehensive_results.csv` - Full results for all phrases and all models
- `cli/bur_comprehensive_cli.py` - CLI tool to run comprehensive analysis
- `analysis/bur_surge_analysis.py` - Statistical functions for all model types

## Usage

```bash
# Run comprehensive analysis
export PYTHONPATH=/Users/achiriboga/Documents/PhraseBurAnalysis-main:$PYTHONPATH
/path/to/.venv/bin/python cli/bur_comprehensive_cli.py

# Or with default settings
echo "20" | /path/to/.venv/bin/python cli/bur_comprehensive_cli.py
```

## Statistical Notes

- All models use FDR correction (Benjamini-Hochberg) at α = 0.05
- Minimum phrase length: 6 BUR values
- Step change minimum threshold: 0.1 BUR units
- End-surge uses last 25% of phrase
- Cohen's d reported for effect size interpretation
