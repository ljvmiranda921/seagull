# -*- coding: utf-8 -*-

# Import standard library
from typing import Callable

# Import modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

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

    def run(self, rule: Callable, iters: int) -> np.ndarray:
        """Run the simulation for a given number of iterations

        Parameters
        ----------
        rule : callable
            Callable that takes in an array and returns an array of the same
            shape.
        iters : int
            Number of iterations to run the simulation.

        Returns
        -------
        numpy.ndarray
            Simulation history
        """
        for i in range(iters):
            self.board.state = rule(self.board.state)
            self.history.append(self.board.state)

        return self.get_history()

    def get_history(self) -> np.ndarray:
        return np.asarray(self.history)

    def animate(self, figsize=(5, 5), interval=100) -> animation.FuncAnimation:
        """Animate the resulting simulation

        Parameters
        ----------
        figsize : tuple
            Size of the output figure
        interval : int
            Interval for transitioning between frames

        Returns
        -------
        matplotlib.animation.FuncAnimation
            Animation generated from the run
        """
        if not self.history:
            raise ValueError("The run() argument must be executed first")

        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
        X_blank = np.zeros(self.board.size, dtype=bool)
        im = ax.imshow(X_blank, cmap=plt.cm.binary, interpolation="nearest")
        im.set_clim(-0.05, 1)

        def _animate(i, history):
            current_pos = history[i]
            im.set_data(current_pos)
            return (im,)

        def _init():
            im.set_data(X_blank)
            return (im,)

        history = self.get_history()
        anim = animation.FuncAnimation(
            fig,
            func=_animate,
            frames=range(history.shape[0]),
            init_func=_init,
            interval=interval,
            fargs=(history,),
            blit=True,
        )
        return anim
