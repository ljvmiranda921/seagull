# -*- coding: utf-8 -*-

"""Growers are lifeforms that exhibit asymptotically unbounded growth"""

# Import modules
import numpy as np

from .base import Lifeform


class Unbounded(Lifeform):
    """A lifeform with asymptotically unbounded growth"""

    def __init__(self):
        """Initialize the class"""
        super(Unbounded, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [
                [1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1],
                [0, 1, 1, 0, 1],
                [1, 0, 1, 0, 1],
            ]
        )
