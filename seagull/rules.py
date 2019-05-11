# -*- coding: utf-8 -*-

"""Rules determine how the evolution of the lifeforms will progress. In
Seagull, rules are implemented as a function that takes in a 2-dimensional
array of a given shape then returns the updated array with the rule applied"""

# Import modules
import numpy as np
import scipy.signal


def conway_classic(X) -> np.ndarray:
    """The classic Conway's Rule for Game of Life

    The classic conway rule states the following:
        1. Any live cell with fewer than two live neighbours dies (exposure)
        2. Any live cell with more than three live neighbours dies (overcrowding)
        3. Any live cell with two or three live neighbours lives, unchanged, to the next generation.
        4. Any dead cell with exactly three live neighbours will come to life

    """
    nbrs_count = (
        scipy.signal.convolve2d(X, np.ones((3, 3)), mode="same", boundary="wrap") - X
    )
    return (nbrs_count == 3) | (X & (nbrs_count == 2))
