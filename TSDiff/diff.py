import numpy as np


def diff(ts: np.array, step: int) -> np.array:
    diff_ts = (ts - np.roll(ts, step))[step:]
    return diff_ts


def undiff(ts: np.array, first_values: np.array) -> np.array:
    first_values = np.array(first_values)
    step = len(first_values)
    undiff_ts = np.append(first_values, ts)
    for i in range(len(ts)):
        undiff_ts[i + step] += undiff_ts[i]
    return undiff_ts
