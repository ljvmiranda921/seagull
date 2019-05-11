# -*- coding: utf-8 -*-

"""Static lifeforms do not oscillate nor move given classic Conway rules"""

# Import modules
import numpy as np

from .base import Lifeform


class Box(Lifeform):
    """A static Box"""

    def __init__(self):
        """Initialize the class"""
        super(Box, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.ones(shape=(2, 2), dtype=int)


class Seed(Lifeform):
    """A static Seed"""

    def __init__(self):
        """Initialize the class"""
        super(Seed, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]])


class Moon(Lifeform):
    """A static Moon"""

    def __init__(self):
        """Initialize the class"""
        super(Moon, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]]
        )


class Kite(Lifeform):
    """A static Kite"""

    def __init__(self):
        """Initialize the class"""
        super(Kite, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[1, 1, 0], [1, 0, 1], [0, 1, 0]])
