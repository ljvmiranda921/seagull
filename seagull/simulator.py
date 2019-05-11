# -*- coding: utf-8 -*-

"""The Simulator takes in a :obj:`seagull.Board`, and runs a simulation given a
set number of iterations and a rule. For each iteration, the rule is applied to
the Board in order to evolve the lifeforms. After the simulation, run
statistics are returned.

.. code-block:: python

    import seagull as sg

    board = sg.Board()
    board.add(Blinker(), loc=(0,0))

    # Initialize a simulator
    sim = sg.Simulator(board)
    stats = sim.run(sg.rules.conway_classic, iters=1000)

Various statistics such as entropy, peak cell coverage, and the like are
returned as a dictionary. This gives us an idea on the characteristics of the
simulation experiment.

.. note::

    Some statistics are highly-dependent on the size of the board and the
    number of iterations. For example, peak cell coverage (pertaining to the
    max. amount of active cells during the whole run) depends on board size. If
    you have better ideas for computing these statistics, please open-up an
    Issue!

The :code:`run()` method only computes the progress of the board for the whole
simulation, but it does not animate it yet. To create an animation, call the
:code:`animate()` method:

.. code-block:: python

    sim.animate()


This returns a :obj:`matplotlib.animation.FuncAnimation` that you can turn into
an interactive animation in your notebook or exported as a GIF.

.. note::

    When exporting to GIF, it is required to have the ffmpeg backend installed.

"""

# Import standard library
from typing import Callable, Union

# Import modules
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from matplotlib import animation

from .board import Board
from .utils import statistics as stats


class Simulator:
    def __init__(self, board: Board):
        """Initialize the class

        Parameters
        ----------
        board : seagull.Board
            The board to run the simulation on
        """
        self.board = board
        self.history = []  # type: list
        self.stats = {}    # type: dict

    def run(self, rule: Callable, iters: int) -> dict:
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
        dict
           Computed statistics for the simulation run
        """
        # Run simulation
        for i in range(iters):
            self.board.state = rule(self.board.state)
            self.history.append(self.board.state)

        self.stats = self.compute_statistics(self.get_history())
        return self.stats

    def compute_statistics(self, history: Union[list, np.ndarray]) -> dict:
        """Compute various statistics for the board

        Parameters
        ----------
        history : list or numpy.ndarray
            The simulation history

        Returns
        -------
        dict
            Compute statistics
        """
        logger.info("Computing simulation statistics...")
        sim_stats = {
            "peak_cell_coverage": np.max(
                [stats.cell_coverage(h) for h in history]
            ),
            "avg_cell_coverage": np.mean(
                [stats.cell_coverage(h) for h in history]
            ),
            "avg_shannon_entropy": np.mean(
                [stats.shannon_entropy(h) for h in history]
            ),
            "peak_shannon_entropy": np.max(
                [stats.shannon_entropy(h) for h in history]
            ),
        }

        return sim_stats

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
            msg = "The run() argument must be executed first"
            logger.error(msg)
            raise ValueError(msg)

        logger.info("Rendering animation...")
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
