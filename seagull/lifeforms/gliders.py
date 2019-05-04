# -*- coding: utf-8 -*-

# Import modules
import numpy as np

from .base import Lifeform


class Glider(Lifeform):
    def __init__(self):
        """Initialize the class"""
        super(Glider, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0]])
