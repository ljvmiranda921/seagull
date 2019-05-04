# -*- coding: utf-8 -*-

# Import standard library
from typing import Callable

import numpy as np

from .board import Board


class Simulator:
    def __init__(self, board: Board):
        """Initialize the class

        Parameters
        ----------
        board : seagull.Board
            The board to run the simulation on
        """
        self.board = board
        self.history = []

    def run(self, rule: Callable, iters: int, save_history: False):
        """Run the simulation

        Parameters
        ----------
        rule : callable
            Callable that takes in an array and returns an array of the same
            shape
        iters : int
            Number of iterations to run the simulation. You can pass `-1` for
            an infinite stream.
        save_history: bool
            Save history as a list of arrays. You can access the history
            through the `self.history` attribute.
        """

        for i in range(iters):
            self.board.state = rule(self.board.state)
            if save_history:
                self.history.append(self.board.state)

    def get_history(self) -> np.array:
        """Get simulation history

        Returns
        -------
        np.array
            Array of shape `(iters, (board.size))``
        """
        return np.asarray(self.history)
