# -*- coding: utf-8 -*-

# Import modules
import numpy as np

from .base import Lifeform


class Blinker(Lifeform):
    """A horizontal Blinker lifeform"""

    def __init__(self, length: int):
        """Initialize the class

        Parameters
        ----------
        length : int
            Length of the blinker
        """
        super(Blinker, self).__init__()
        self.length = length

    @property
    def layout(self) -> np.ndarray:
        return np.ones(shape=(self.length, 1), dtype=int)


class Toad(Lifeform):
    """A Toad lifeform oscillator"""

    def __init__(self):
        """Initialize the class"""
        super(Toad, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[1, 1, 1, 0], [0, 1, 1, 1]])
