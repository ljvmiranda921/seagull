# -*- coding: utf-8 -*-

"""Base class for all Lifeform implementations. All lifeforms found in this
library inherits from the :obj:`seagull.lifeforms.base.Lifeform` class. You can
use this to implement your own lifeforms or contributing new lifeforms to
Seagull:

    .. code-block:: python

        class MyNewLifeform(Lifeform):

            def __init__(self, arg1=1, arg2=2):
                super(MyNewLifeform, self).__init__()
                self.arg1 = arg1
                self.arg2 = arg2

            @property
            def layout(self) -> np.ndarray:
                return np.array([[0, 0, 1, 1]])

When contributing your new lifeform, we highly-recommend to set sensible
defaults when initializing it. This is because the current test running simply
runs the :mod:`inspect` module to get all  classes and run the same set of
tests.


If you wish to pass a custom lifeform to the board, I recommend using the
:obj:`seagull.lifeforms.custom.Custom` class.
"""


# Import standard library
import abc
from typing import Dict, Tuple, Union

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.image import AxesImage


class Lifeform(abc.ABC):
    """Base class for all Lifeform implementation"""

    @abc.abstractproperty
    def layout(self) -> np.ndarray:
        """:obj:`numpy.ndarray`: Lifeform layout or structure"""
        pass

    @property
    def size(self) -> Tuple[int, int]:
        """:obj:`tuple`: Size of the lifeform"""
        return self.layout.shape

    def view(self, figsize=(5, 5)) -> Tuple[Figure, AxesImage]:
        """View the lifeform


        Returns
        -------
        matplotlib.axes._subplots.AxesSubplot
            Graphical view of the lifeform
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
        im = ax.imshow(
            self.layout, cmap=plt.cm.binary, interpolation="nearest"
        )
        im.set_clim(-0.05, 1)
        return fig, im
