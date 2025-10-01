"""
Configuration constants for PhraseBur analysis.
"""

# Minimum number of BUR values required for statistical analysis
# This ensures adequate degrees of freedom:
# - Linear regression: n-2 degrees of freedom, so n=6 gives 4 d.f.
# - Phrase structure: middle section needs multiple values for std dev
# - Variation analysis: std with ddof=1 needs adequate sample size
MIN_BUR_VALUES = 6
