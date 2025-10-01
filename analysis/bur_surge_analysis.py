"""
BUR Surge Analysis - Linear Trend Detection

Performs simple linear regression on BUR values across phrase positions
to detect trends (increases/decreases) in swing timing within phrases.
"""

import numpy as np
from scipy import stats
from utils.config import MIN_BUR_VALUES, CONFIDENCE_LEVEL, LINEAR_REGRESSION_PARAMS, FDR_ALPHA


def linear_trend_analysis(bur_values):
    """
    Perform linear regression on BUR values to detect trends.
    
    Args:
        bur_values: List or array of BUR values in temporal order
        
    Returns:
        Dictionary containing:
            - slope: Rate of BUR change per position
            - intercept: BUR value at position 0
            - r2: Coefficient of determination (proportion of variance explained)
            - p_value: Significance of the slope (null hypothesis: slope = 0)
            - std_err: Standard error of the slope
            - conf_interval: Confidence interval for the slope (default 95%)
            - direction: 'increase', 'decrease', or 'none'
            - n_values: Number of BUR values
            
    Note:
        - Uses scipy.stats.linregress for regression
        - p_value tests H0: slope = 0 (no trend) with two-tailed test
        - Confidence interval uses t-distribution with n-2 degrees of freedom
        - Assumes independence of observations (potential limitation)
    """
    n = len(bur_values)
    if n < MIN_BUR_VALUES:
        return None
        
    x = np.arange(n)
    y = np.array(bur_values, dtype=float)
    
    # Perform linear regression
    result = stats.linregress(x, y)
    
    # Calculate confidence interval for slope
    # For a two-tailed test with confidence_level (e.g., 95%), we need the
    # critical value at (1 + confidence_level) / 2 = 0.975 for 95%
    # This accounts for splitting alpha/2 into each tail
    alpha = 1 - CONFIDENCE_LEVEL
    t_percentile = 1 - alpha / 2  # 0.975 for 95% CI
    df = n - LINEAR_REGRESSION_PARAMS  # degrees of freedom
    t_critical = stats.t.ppf(t_percentile, df)
    ci_lower = result.slope - t_critical * result.stderr # type: ignore
    ci_upper = result.slope + t_critical * result.stderr # type: ignore
    
    # Determine direction
    if result.slope > 0: # type: ignore
        direction = 'increase'
    elif result.slope < 0: # type: ignore
        direction = 'decrease'
    else:
        direction = 'none'
    
    return {
        'slope': result.slope, # type: ignore
        'intercept': result.intercept, # type: ignore
        'r2': result.rvalue ** 2, # type: ignore
        'p_value': result.pvalue, # type: ignore
        'std_err': result.stderr, # type: ignore
        'conf_interval': (ci_lower, ci_upper),
        'direction': direction,
        'n_values': n
    }


def fdr_correction(p_values, alpha=FDR_ALPHA):
    """
    Apply Benjamini-Hochberg FDR correction for multiple testing.
    
    Args:
        p_values: List of p-values to correct
        alpha: Desired false discovery rate (default from config: 0.05)
        
    Returns:
        Tuple of (reject, p_values_corrected)
            - reject: Boolean array indicating which tests to reject
            - p_values_corrected: FDR-corrected p-values
            
    Note:
        Uses Benjamini-Hochberg procedure to control false discovery rate.
        This is less conservative than Bonferroni correction and more
        appropriate when testing many hypotheses.
    """
    from statsmodels.stats.multitest import multipletests
    
    # Remove None values for correction
    valid_p_values = [p for p in p_values if p is not None]
    
    if len(valid_p_values) == 0:
        return [], []
    
    # Apply FDR correction
    reject, p_corrected, _, _ = multipletests(
        valid_p_values, 
        alpha=alpha, 
        method='fdr_bh'  # Benjamini-Hochberg
    )
    
    return reject, p_corrected
