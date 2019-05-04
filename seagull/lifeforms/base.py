# -*- coding: utf-8 -*-

"""Base class for all Lifeform implementations"""


# Import standard library
import abc
from typing import Dict, Tuple, Union

# Import modules
import numpy as np
from matplotlib.axes._subplots import (Axes, Subplot)


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

    def view(self) -> Union[Axes, Subplot]:
        """View the lifeform


        Returns
        -------
        matplotlib.axes._subplots.AxesSubplot
            Graphical view of the lifeform
        """
        pass
