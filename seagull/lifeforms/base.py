# -*- coding: utf-8 -*-

"""Base class for all Lifeform implementations"""


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
        """numpy.ndarray: Lifeform layout or structure"""
        pass

    @property
    def size(self) -> Tuple[int, int]:
        """tuple: Size of the lifeform"""
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
        im = ax.imshow(self.layout, cmap=plt.cm.binary, interpolation="nearest")
        im.set_clim(-0.05, 1)
        return fig, im

