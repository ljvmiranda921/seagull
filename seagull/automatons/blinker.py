# -*- coding: utf-8 -*-

# Import standard library
from typing import Dict, Tuple

# Import modules
import numpy as np

from .base import Automaton


class Blinker(Automaton):
    """A horizontal Blinker automaton"""

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
        return np.ones(shape=(self.length,), dtype=int)

