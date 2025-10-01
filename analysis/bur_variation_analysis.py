import numpy as np
from utils.data_utils import get_artist_from_id
from utils.config import MIN_BUR_VALUES

def phrase_variation_stats(bur_values):
    n = len(bur_values)
    if n < MIN_BUR_VALUES:
        return None
    std_bur = np.std(bur_values, ddof=1)
    return {
        'n_values': n,
        'std_bur': std_bur
    }
