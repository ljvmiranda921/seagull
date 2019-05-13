# -*- coding: utf-8 -*-

# Import modules
import pytest
import numpy as np
from matplotlib import animation


# Import from package
from seagull import lifeforms as lf
import seagull as sg


def test_simulator_run():
    """Test if the run() method returns the computed statistics"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    sim = sg.Simulator(board)
    stats = sim.run(sg.rules.conway_classic, iters=10)
    assert isinstance(stats, dict)


@pytest.mark.parametrize("exclude_init", [True, False])
def test_simulator_get_history_shape(exclude_init):
    """Test if get_history() will return the expected shape"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    sim = sg.Simulator(board)
    sim.run(sg.rules.conway_classic, iters=10)
    hist = sim.get_history(exclude_init)
    expected_depth = 10 if exclude_init else 11
    assert hist.shape == (expected_depth, 10, 10)


def test_simulator_animate():
    """Test if animate() method returns a FuncAnimation"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    sim = sg.Simulator(board)
    sim.run(sg.rules.conway_classic, iters=10)
    anim = sim.animate()
    assert isinstance(anim, animation.FuncAnimation)


def test_simulator_animate_without_run():
    """Test if animate() method throws an error when called before run()"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    sim = sg.Simulator(board)
    with pytest.raises(ValueError):
        sim.animate()


def test_compute_statistics():
    """Test if compute_statistics() returns a dictionary"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    sim = sg.Simulator(board)
    sim.run(sg.rules.conway_classic, iters=10)
    stats = sim.compute_statistics(sim.get_history())
    assert isinstance(stats, dict)


def test_simulator_inplace():
    """Test if board state didn't change after a simulation run"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Glider(), loc=(0, 0))

    # Initial board state, must be the same always
    init_board = board.state.copy()

    # Run simulator
    sim = sg.Simulator(board)
    sim.run(sg.rules.conway_classic, iters=10)
    assert np.array_equal(board.state, init_board)
