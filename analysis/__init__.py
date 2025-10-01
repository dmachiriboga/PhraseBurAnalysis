"""
Analysis modules for statistical calculations, model fitting, and trend detection.
"""

from .bur_surge_analysis import (
    exp_func,
    log_func,
    fit_and_evaluate_models
)

from .bur_phrase_structure_analysis import (
    phrase_structure_stats
)

from .bur_variation_analysis import (
    phrase_variation_stats
)

__all__ = [
    'exp_func',
    'log_func',
    'fit_and_evaluate_models',
    'phrase_structure_stats',
    'phrase_variation_stats'
]
