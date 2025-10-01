"""
Configuration constants for PhraseBur analysis.
"""

# Minimum number of BUR values required for statistical analysis
# This ensures adequate degrees of freedom:
# - Linear regression: n-2 degrees of freedom, so n=6 gives 4 d.f.
# - Phrase structure: middle section needs multiple values for std dev
# - Variation analysis: std with ddof=1 needs adequate sample size
MIN_BUR_VALUES = 6

# Statistical confidence level for confidence intervals
# 0.95 = 95% confidence level (standard in research)
CONFIDENCE_LEVEL = 0.95

# Number of parameters in linear regression (slope + intercept)
# Used to calculate degrees of freedom: df = n - LINEAR_REGRESSION_PARAMS
LINEAR_REGRESSION_PARAMS = 2

# False Discovery Rate (FDR) alpha level for multiple testing correction
# 0.05 = 5% false discovery rate (standard threshold)
FDR_ALPHA = 0.05
