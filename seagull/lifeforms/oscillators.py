# -*- coding: utf-8 -*-

"""Oscillators are lifeforms that returns to its initial configuration after
some time"""

# Import modules
import numpy as np

from .base import Lifeform


class Blinker(Lifeform):
    """A horizontal Blinker lifeform

    A `Blinker <https://www.conwaylife.com/wiki/Blinker>`_ by John Conway,
    the smallest and most common oscillator there is (period 2).
    """

    def __init__(self, length=3):
        """Initialize the class

        Parameters
        ----------
        length : int
            Length of the blinker. Default is 3
        """
        super(Blinker, self).__init__()
        self.length = length

    @property
    def layout(self) -> np.ndarray:
        return np.ones(shape=(self.length, 1), dtype=int)


class Toad(Lifeform):
    """A Toad lifeform oscillator

    A `Toad <https://www.conwaylife.com/wiki/Toad>`_ by Simon Norton, the
    second most common oscillator after the blinker (period 2).
    """

    def __init__(self):
        """Initialize the class"""
        super(Toad, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        return np.array([[1, 1, 1, 0], [0, 1, 1, 1]])


class Pulsar(Lifeform):
    """A Pulsar lifeform oscillator

    A `Pulsar <https://www.conwaylife.com/wiki/Pulsar>`_ by John Conway, the
    fourth most common oscillator overall and by far the most common one
    with a period greater than 2 (period 3).
    """

    def __init__(self):
        """Initialize the class"""
        super(Pulsar, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((17, 17))
        X[2, 4:7] = 1
        X[4:7, 7] = 1
        X += X.T
        X += X[:, ::-1]
        X += X[::-1, :]
        return X


class FigureEight(Lifeform):
    """A Figure eight lifeform oscillator

    A period 8 oscillator. See
    `Figure eight <https://www.conwaylife.com/wiki/Figure_eight>`_.
    """

    def __init__(self):
        """Initialize the class"""
        super(FigureEight, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((6, 6))
        X[0:3, 0:3] = 1
        X[3:6, 3:6] = 1
        return X


class Beacon(Lifeform):
    """A Beacon lifeform oscillator

    A `Beacon <https://www.conwaylife.com/wiki/Beacon>`_ by John Conway, a
    common period 2 oscillator.
    """

    def __init__(self):
        """Initialize the class"""
        super(Beacon, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((4, 4))
        X[0:2, 0:2] = 1
        X[2:4, 2:4] = 1
        return X


class Pentadecathlon(Lifeform):
    """ A Pentadecathlon lifeform oscillator

    The most natural oscillator of period greater than 3: 10 cells placed in
    a row evolve into this object, the fifth or sixth most common oscillator
    overall. See
    `Pentadecathlon <https://www.conwaylife.com/wiki/Pentadecathlon>`_.
    """

    def __init__(self):
        """Initialize the class"""
        super(Pentadecathlon, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.ones(shape=(8, 3), dtype=int)
        X[1, 1] = 0
        X[6, 1] = 0
        return X


class ChaCha(Lifeform):
    """A Cha Cha lifeform oscillator

    A period 2 oscillator named for the dance. See
    `Cha cha <https://www.conwaylife.com/wiki/Cha_cha>`_.
    """

    def __init__(self):
        """Initialize the class"""
        super(ChaCha, self).__init__()

    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((6, 8))
        X[0, 4] = 1
        X[1, 2::2] = 1
        X[2, ::2] = 1
        X += np.rot90(X, 2)
        return X
