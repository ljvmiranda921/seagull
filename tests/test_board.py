# -*- coding: utf-8 -*-

# Import modules
import numpy as np
import pytest
from matplotlib.figure import Figure
from matplotlib.image import AxesImage

# Import from package
from seagull import lifeforms as lf
from seagull.board import Board


def test_board_add():
    """Test if adding a lifeform to board is successful"""
    board = Board(size=(3, 3))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    assert np.array_equal(board.state, np.array([[False, True, False]] * 3))


def test_board_add_out_of_bounds():
    """Test if adding an out-of-bounds lifeform to board will raise an error"""
    board = Board(size=(5, 5))
    with pytest.raises(ValueError):
        board.add(lf.Pulsar(), loc=(0, 2))


def test_board_clear():
    """Test if the board resets whenever clear is called"""
    board = Board(size=(3, 3))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    board.clear()
    assert len(np.unique(board.state)) == 1
    assert np.unique(board.state)[0].astype(int) == 0


def test_board_view():
    """Test if a figure and image is returned whenever view is called"""
    board = Board(size=(3, 3))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    fig, im = board.view()
    assert isinstance(fig, Figure)
    assert isinstance(im, AxesImage)
