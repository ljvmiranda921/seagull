# -*- coding: utf-8 -*-

# Import standard library
from typing import Union

# Import modules
import numpy as np
from loguru import logger

from .base import Lifeform


class Custom(Lifeform):
    """Create custom lifeforms"""

    def __init__(self, X: Union[np.ndarray, list]):
        """Initialize the class

        Parameters
        ----------
        X : array_like
            Custom binary array for the lifeform
        """
        self.validate_input_values(np.array(X))
        self.validate_input_shapes(np.array(X))
        self.X = X

    def validate_input_values(self, X: np.ndarray):
        """Check if all elements are binary"""
        if not ((X == 0) | (X == 1) | (X is True) | (X is False)).all():
            msg = "Input array should only contain {0,1} or {True,False}"
            logger.error(msg)
            raise ValueError(msg)

    def validate_input_shapes(self, X: np.ndarray):
        """Check if input array is of size 2"""
        if X.ndim != 2:
            msg = (
                "Input array should have 2 dimensions: {} != 2. "
                "For a 1-d lifeform, please add a new axis".format(X.ndim)
            )
            logger.error(msg)
            raise ValueError(msg)

    @property
    def layout(self) -> np.ndarray:
        return np.array(self.X)
