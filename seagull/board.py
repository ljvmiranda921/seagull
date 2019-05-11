# -*- coding: utf-8 -*-

"""The Board represents the environment where lifeforms can evolve, you can
initialize a Board by passing a tuple representing its size:

.. code-block:: python

    import seagull as sg
    board = sg.Board(size=(30, 30))  # default is (100, 100)

You can add lifeforms to the board by using the :code:`add()` command. You
should pass an instance of the lifeform and its location on the board. The
`loc` parameter is anchored at the top-left for two-dimensional lifeforms and
to the left for one-dimensional lifeforms. It follows numpy's `indexing
convention <https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html>`_

Whenever a lifeform's size exceeds the edge of the board, then Seagull throws a
:code:`ValueError`:

.. code-block:: python

    import seagull as sg
    board = sg.Board()
    board.add(sg.lifeforms.Blinker(length=3), loc=(0,0))

You can always view the board's state by calling the :code:`view()` method.
Lastly, you can clear the board with the :code:`clear()` command.

"""

# Import standard library
from typing import Tuple

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from loguru import logger

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
        self.state = np.zeros(size, dtype=bool)

    def add(self, lifeform: Lifeform, loc: Tuple[int, int]):
        """Add a lifeform to the board

        Parameters
        ----------
        lifeform: :obj:`seagull.lifeforms.base.Lifeform`
            A lifeform that can evolve in the board
        loc : array_like of size 2
            Initial location of the lifeform on the board
        """
        try:
            row, col = loc
            height, width = lifeform.size
            self.state[row : row + height, col : col + width] = lifeform.layout
        except ValueError:
            logger.error("Lifeform is out-of-bounds!")
            raise

    def clear(self):
        """Clear the board and remove all lifeforms"""
        logger.debug("Board cleared!")
        self.state = np.zeros(self.size, dtype=bool)

    def view(self, figsize=(5, 5)) -> Tuple[Figure, AxesImage]:
        """View the current state of the board

        Parameters
        ----------
        figsize : tuple
            Size of the output figure

        Returns
        -------
        (:obj:`matplotlib.figure.Figure`, :obj:`matplotlib.image.AxesImage`)
            Graphical view of the board
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
        im = ax.imshow(self.state, cmap=plt.cm.binary, interpolation="nearest")
        im.set_clim(-0.05, 1)
        return fig, im
