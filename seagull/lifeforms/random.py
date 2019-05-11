# -*- coding: utf-8 -*-

"""Random lifeforms are generated on-the-fly without specific configuration"""

# Import standard library
from typing import Tuple

# Import modules
import numpy as np

from .base import Lifeform


class RandomBox(Lifeform):
    """A random box with arbitrarily-set shape"""

    def __init__(self, shape=(3, 3), seed=None):
        """Initialize the class

        Parameters
        ----------
        shape : tuple
            Coverage of the random box
        seed : int, optional
            Random seed
        """
        super(RandomBox, self).__init__()
        self.shape = shape
        self.seed = seed

    @property
    def layout(self) -> np.ndarray:
        np.random.seed(self.seed)
        return np.random.choice([0, 1], size=self.shape)
