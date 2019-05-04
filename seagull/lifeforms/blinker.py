# -*- coding: utf-8 -*-

# Import standard library
from typing import Dict, Tuple

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
