# -*- coding: utf-8 -*-

"""Rules determine how the evolution of the lifeforms will progress. In
Seagull, rules are implemented as a function that takes in a 2-dimensional
array of a given shape then returns the updated array with the rule applied"""

# Import standard library
import re
from typing import Tuple, List

# Import modules
import numpy as np
from scipy.signal import convolve2d
from loguru import logger

# Import from package


def conway_classic(X) -> np.ndarray:
    """The classic Conway's Rule for Game of Life (B3/S23)"""
    return life_rule(X, rulestring="B3/S23")


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
    birth_req, survival_req = _parse_rulestring(rulestring)
    neighbors = _count_neighbors(X)
    birth_rule = (X == 0) & (np.isin(neighbors, birth_req))
    survival_rule = (X == 1) & (np.isin(neighbors, survival_req))
    return birth_rule | survival_rule


def _parse_rulestring(r: str) -> Tuple[List[int], List[int]]:
    """Parse a rulestring"""
    pattern = re.compile("B([0-8]+)?/S([0-8]+)?")
    if pattern.match(r):
        birth, survival = r.split("/")
        birth_neighbors = [int(s) for s in birth if s.isdigit()]
        survival_neighbors = [int(s) for s in survival if s.isdigit()]
    else:
        msg = f"Rulestring ({r}) must satisfy the pattern {pattern}"
        logger.error(msg)
        raise ValueError(msg)

    return birth_neighbors, survival_neighbors


def _count_neighbors(X: np.ndarray) -> np.ndarray:
    """Get the number of neighbors in a binary 2-dimensional matrix"""
    n = convolve2d(X, np.ones((3, 3)), mode="same", boundary="wrap") - X
    return n
