# -*- coding: utf-8 -*-

# Import modules
import numpy as np
from scipy.signal import convolve2d


def conway_classic(X):
    """The classic Conway's Rule for Game of Life"""
    nbrs_count = (
        convolve2d(X, np.ones((3, 3)), mode="same", boundary="wrap") - X
    )
    return (nbrs_count == 3) | (X & (nbrs_count == 2))
