"""
Analysis modules for statistical calculations, model fitting, and trend detection.
"""

from .bur_surge_analysis import (
    linear_trend_analysis,
    fdr_correction
)

from .bur_phrase_structure_analysis import (
    phrase_structure_stats
)

from .bur_variation_analysis import (
    phrase_variation_stats
)

__all__ = [
    'linear_trend_analysis',
    'fdr_correction',
    'phrase_structure_stats',
    'phrase_variation_stats'
]
