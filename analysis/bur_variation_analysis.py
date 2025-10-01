import numpy as np
from utils.data_utils import get_artist_from_id

def phrase_variation_stats(bur_values):
    n = len(bur_values)
    if n < 2:
        return None
    std_bur = np.std(bur_values, ddof=1)
    return {
        'n_values': n,
        'std_bur': std_bur
    }
