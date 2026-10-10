# -*- coding: utf-8 -*-

"""Static lifeforms do not oscillate nor move given classic Conway rules"""

# Import modules
import numpy as np

from .base import Lifeform


class Box(Lifeform):
    """A static Box

    This is the `Block <https://www.conwaylife.com/wiki/Block>`_, an
    extremely common 4-cell still life and the smallest one there is.
    """

    def __init__(self):
        """Initialize the class"""
        super(Box, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.ones(shape=(2, 2), dtype=int)


class Seed(Lifeform):
    """A static Seed

    The layout is the `Beehive <https://www.conwaylife.com/wiki/Beehive>`_,
    an extremely common 6-cell still life.
    """

    def __init__(self):
        """Initialize the class"""
        super(Seed, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]])


class Moon(Lifeform):
    """A static Moon, a 7-cell still life"""

    def __init__(self):
        """Initialize the class"""
        super(Moon, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]]
        )


class Kite(Lifeform):
    """A static Kite, a 5-cell still life"""

    def __init__(self):
        """Initialize the class"""
        super(Kite, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[1, 1, 0], [1, 0, 1], [0, 1, 0]])


class Eater1(Lifeform):
    """A static Eater

    This is `Eater 1 <https://www.conwaylife.com/wiki/Eater_1>`_, the first
    discovered eater and a 7-cell still life. It can absorb a glider without
    being damaged, which is what makes it useful.
    """

    def __init__(self):
        """Initialize the class"""
        super(Eater1, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [[1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1]]
        )


class SwitchEngine(Lifeform):
    """A Switch engine lifeform

    The layout is the `Switch engine
    <https://www.conwaylife.com/wiki/Switch_engine>`_ by Charles Corderman,
    a methuselah with lifespan 3911 that can be used to build c/12 diagonal
    puffers and spaceships. Despite living in this module it is *not* a still
    life: it grows, so applying a rule to it keeps changing the board.
    """

    def __init__(self):
        """Initialize the class"""
        super(SwitchEngine, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array(
            [
                [0, 1, 0, 1, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0],
                [0, 0, 0, 1, 1, 1],
            ]
        )
