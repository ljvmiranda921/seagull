# -*- coding: utf-8 -*-

"""Rules determine how the evolution of the lifeforms will progress. In
Seagull, rules are implemented as a function that takes in a 2-dimensional
array of a given shape then returns the updated array with the rule applied"""

# Import standard library
from typing import Tuple, List

# Import modules
import numpy as np
from scipy.signal import convolve2d
from loguru import logger

# Import from package


def conway_classic(X) -> np.ndarray:
    """The classic Conway's Rule for Game of Life

    The classic conway rule states the following:
        1. Any live cell with fewer than two live neighbours dies (exposure)
        2. Any live cell with more than three live neighbours dies (overcrowding)
        3. Any live cell with two or three live neighbours lives, unchanged, to the next generation.
        4. Any dead cell with exactly three live neighbours will come to life

    """
    nbrs_count = (
        convolve2d(X, np.ones((3, 3)), mode="same", boundary="wrap") - X
    )
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


def life_rule(X: np.ndarray, rulestring: str) -> np.ndarray:
    """A generalized life rule that accepts a rulestring in B/S notation

    Rulestrings are commonly expressed in the B/S notation where B (birth) is a
    list of all numbers of live neighbors that cause a dead cell to come alive,
    and S (survival) is a list of all the numbers of live neighbors that cause
    a live cell to remain alive.

    Parameters
    ----------
    X : np.ndarray
        The input board matrix
    rulestring : str
        The rulestring in B/S notation

    Returns
    -------
    np.ndarray
        Updated board after applying the rule
    """
    birth, survival = _parse_rulestring(rulestring)
    neighbors = _count_neighbors(X)
    birth_rule = (X == 0) & (neighbors in birth)
    survival_rule = (X == 1) & (neighbors in survival)
    return birth_rule | survival_rule


def _parse_rulestring(r: str) -> Tuple[List[int], List[int]]:
    """Parse a rulestring"""
    try:
        birth, survival = r.split("/")
        birth_neighbors = [int(s) for s in birth if s.isdigit()]
        survival_neighbors = [int(s) for s in survival if s.isdigit()]
    except Exception as e:
        msg = f"Cannot parse rulestring {r}: {e}"
        logger.error(msg)
        print(msg)
        raise
    return birth_neighbors, survival_neighbors


def _count_neighbors(X: np.ndarray) -> np.ndarray:
    """Get the number of neighbors in a binary 2-dimensional matrix"""
    n = convolve2d(X, np.ones((3, 3)), mode="same", boundary="wrap") - X
    return n
