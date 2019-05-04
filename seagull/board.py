# -*- coding: utf-8 -*-

# Import standard library
from typing import Tuple, Union

# Import modules
import numpy as np
from loguru import logger
from matplotlib.axes._subplots import (Axes, Subplot)
from scipy.sparse import lil_matrix

from .lifeforms.base import Lifeform


class Board:
    """Represents the environment where the lifeforms can grow and evolve"""

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
    def add(self, lifeform: Lifeform, loc: Tuple[float, float]):
        """Add a lifeform to the board

        Parameters
        ----------
        lifeform: seagull.Lifeform
            A lifeform that can evolve in the board
        loc : array_like of size 2
            Initial location of the lifeform
        """
        # TODO: get the size of the lifeform from its property, and use that
        # for setting the values. Some gotchas you need to consider:
        # * Cases when the size is just 1-dimensional
        # * Raise an error whenever the resulting dimension exceeds that of the
        #   board
        pass

    def clear(self):
        """Clear the board and remove all lifeforms"""
        self.state = lil_matrix(self.size, dtype=bool)

    def view(self) -> Union[Axes, Subplot]:
        """View the current state of the board

        Returns
        -------
        matplotlib.axes._subplots.AxesSubplot
            Graphical view of the board
        """
        pass
