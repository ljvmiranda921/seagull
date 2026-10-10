# -*- coding: utf-8 -*-

"""Gliders are lifeforms that oscillate but move while oscillating"""

# Import modules
import numpy as np

from .base import Lifeform


class Glider(Lifeform):
    """A Glider lifeform

    The `Glider <https://www.conwaylife.com/wiki/Glider>`_ by Richard K. Guy:
    the smallest, most common, and first discovered spaceship. It travels
    diagonally with period 4 and speed c/4.
    """

    def __init__(self):
        """Initialize the class"""
        super(Glider, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[1, 0, 0], [0, 1, 1], [1, 1, 0]])


class LightweightSpaceship(Lifeform):
    """A Lightweight spaceship lifeform

    A `Lightweight spaceship
    <https://www.conwaylife.com/wiki/Lightweight_spaceship>`_ by John Conway,
    a very well-known period 4 c/2 orthogonal spaceship.
    """

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [
                [0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
            ]
        )


class MiddleweightSpaceship(Lifeform):
    """A Middleweight spaceship lifeform

    A `Middleweight spaceship
    <https://www.conwaylife.com/wiki/Middleweight_spaceship>`_ by John Conway,
    a very well-known period 4 c/2 orthogonal spaceship.
    """

    def __init__(self):
        super(MiddleweightSpaceship, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [
                [0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 0],
            ]
        )
