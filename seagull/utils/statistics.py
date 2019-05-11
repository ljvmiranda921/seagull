# -*- coding: utf-8 -*-

"""Statistics contain various computations to characterize a board state"""

import numpy as np


def shannon_entropy(state: np.ndarray) -> float:
    """Compute for the shannon entropy for the whole board

    Parameters
    ----------
    state : :obj:`numpy.ndarray`
        The board state to compute statistics from

    Returns
    -------
    float
        Shannon entropy
    """
    zero_probs = np.count_nonzero(state) / np.product(state.shape)
    one_probs = 1 - zero_probs
    return -np.sum(np.log2([zero_probs, one_probs]))


def cell_coverage(state: np.ndarray) -> float:
    """Compute for the live cell coverage for the whole board

    Parameters
    ----------
    state : :obj:`numpy.ndarray`
        The board state to compute statistics from

    Returns
    -------
    float
        Cell coverage
    """
    return np.sum(state) / np.product(state.shape)
