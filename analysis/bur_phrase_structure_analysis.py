import numpy as np
from utils.data_utils import get_artist_from_id

def phrase_structure_stats(bur_values, threshold=0.4):
    n = len(bur_values)
    if n < 6:
        return None
    first_bur = bur_values[0]
    last_bur = bur_values[-1]
    middle_bur = bur_values[1:-1]
    mean_middle = np.mean(middle_bur)
    std_middle = np.std(middle_bur, ddof=1) if len(middle_bur) > 1 else 0
    first_higher = (first_bur - mean_middle) > threshold
    last_higher = (last_bur - mean_middle) > threshold
    z_first = (first_bur - mean_middle) / std_middle if std_middle > 0 else 0
    z_last = (last_bur - mean_middle) / std_middle if std_middle > 0 else 0
    sig_first = abs(z_first) > 1.96
    sig_last = abs(z_last) > 1.96
    return {
        "first_bur": first_bur,
        "last_bur": last_bur,
        "mean_middle_bur": mean_middle,
        "first_vs_middle": "higher" if first_higher else "lower",
        "last_vs_middle": "higher" if last_higher else "lower",
        "n_values": n,
        "z_first": z_first,
        "z_last": z_last,
        "sig_first": sig_first,
        "sig_last": sig_last
    }
