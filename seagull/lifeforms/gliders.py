# -*- coding: utf-8 -*-

"""Gliders are lifeforms that oscillate but move while oscillating"""

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


class LightweightSpaceship(Lifeform):
    def __init__(self):
        super(LightweightSpaceship, self).__init__()

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


class HeavyweightSpaceship(Lifeform):
    """A Heavyweight spaceship lifeform

    The largest of the three spaceships shipped with Seagull: it travels
    orthogonally at c/2 with a period of 4, just like the lightweight and
    middleweight spaceships. See the Heavyweight spaceship page on
    `LifeWiki <https://www.conwaylife.com/wiki/Heavyweight_spaceship>`_.
    """

    def __init__(self):
        super(HeavyweightSpaceship, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [
                [0, 0, 0, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 0],
            ]
        )
