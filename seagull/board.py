# -*- coding: utf-8 -*-

# Import standard library
from typing import Tuple

# Import modules
import numpy as np
from loguru import logger
from matplotlib.axes._subplots import AxesSubplot
from scipy.sparse import lil_matrix

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
        self.state = lil_matrix(size, dtype=bool)

    @logger.catch
    def add(self, automaton: Automaton, loc: Tuple[float, float]):
        """Add an automaton to the board

        Parameters
        ----------
        automaton: seagull.Automaton
            An automaton that can evolve in the board
        loc : array_like of size 2
            Initial location of the automaton
        """
        # TODO: get the size of the automaton from its property, and use that
        # for setting the values. Some gotchas you need to consider:
        # * Cases when the size is just 1-dimensional
        # * Raise an error whenever the resulting dimension exceeds that of the
        #   board
        pass

    def clear(self):
        """Clear the board and remove all automatons"""
        self.state = lil_matrix(self.size, dtype=bool)

    def view(self) -> AxesSubplot:
        """View the current state of the board

        Returns
        -------
        matplotlib.axes._subplots.AxesSubplot
            Graphical view of the board
        """
        pass
