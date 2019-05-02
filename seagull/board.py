# -*- coding: utf-8 -*-

# Import standard library
from typing import Tuple

# Import modules
import numpy as np
from matplotlib.axes._subplots import AxesSubplot

from .automatons.base import Automaton


class Board:
    """Represents the environment where the automatons can grow and evolve"""

    def __init__(self, size=(100, 100)):
        """Initialize the class

        Parameters
        ----------
        size : array_like of size 2
            Size of the board (default is `(100, 100)`)

        """
        self.size = size
        self.state = np.zero(size, dtype=bool)

    def add(self, automaton: Automaton, anchor: str, loc: Tuple[float, float]):
        """Add an automaton to the board

        Parameters
        ----------
        automaton: seagull.Automaton
            An automaton that can evolve in the board
        anchor : {`top`, `bottom`, `left`, `right`, `center`}
            Anchor for placing the automaton
        loc : array_like of size 2
            Initial location of the automaton when placed
        """
        pass

    def view(self) -> AxesSubplot:
        """View the current state of the board

        Returns
        -------
        matplotlib.axes._subplots.AxesSubplot
            Graphical view of the board
        """
        pass
