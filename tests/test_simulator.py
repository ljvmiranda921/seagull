# -*- coding: utf-8 -*-

# Import modules
import pytest
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


def test_simulator_get_history_shape():
    """Test if get_history() will return the expected shape"""
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    sim = sg.Simulator(board)
    sim.run(sg.rules.conway_classic, iters=10)
    hist = sim.get_history()
    assert hist.shape == (10, 10, 10)


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
