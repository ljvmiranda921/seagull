# -*- coding: utf-8 -*-

"""Methuselahs are long-lived lifeforms which evolve rapidly before reaching
a steady state after many cycles. The steady state may consist of several
oscillators and still lifes."""

# Import modules
import numpy as np

from .base import Lifeform


class Century(Lifeform):
    """A Century Methuselah lifeform"""

    def __init__(self):
        """Initialize the class"""
        super(Century, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((3, 4))
        X[0, 2:] = 1
        X[1, :3] = 1
        X[2, 1] = 1
        return X


class Thunderbird(Lifeform):
    """A Thunderbird Methuselah lifeform"""

    def __init__(self):
        """Initialize the class"""
        super(Thunderbird, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((5, 3))
        X[0, :] = 1
        X[2:, 1] = 1
        return X


class Acorn(Lifeform):
    """An Acorn Methuselah lifeform

    A 7-cell pattern that stabilizes only after 5,206 generations, leaving
    633 live cells behind. See the
    `Acorn <https://www.conwaylife.com/wiki/Acorn>`_ page on LifeWiki.
    """

    def __init__(self):
        """Initialize the class"""
        super(Acorn, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((3, 7))
        X[0, 1] = 1
        X[1, 3] = 1
        X[2, [0, 1, 4, 5, 6]] = 1
        return X


class Rpentomino(Lifeform):
    """An R-pentomino Methuselah lifeform

    The first methuselah ever discovered: it takes 1,103 generations to
    stabilize and produces six escaping gliders on the way. See the
    `R-pentomino <https://www.conwaylife.com/wiki/R-pentomino>`_ page.
    """

    def __init__(self):
        """Initialize the class"""
        super(Rpentomino, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((3, 3))
        X[0, 1:] = 1
        X[1, :2] = 1
        X[2, 1] = 1
        return X


class Diehard(Lifeform):
    """A Diehard Methuselah lifeform

    A 7-cell pattern that disappears completely after exactly 130
    generations. See the
    `Diehard <https://www.conwaylife.com/wiki/Diehard>`_ page on LifeWiki.
    """

    def __init__(self):
        """Initialize the class"""
        super(Diehard, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((3, 8))
        X[0, 6] = 1
        X[1, [0, 1]] = 1
        X[2, [1, 5, 6, 7]] = 1
        return X
