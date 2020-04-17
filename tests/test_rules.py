# -*- coding: utf-8 -*-

# Import standard library
from typing import Tuple, List

# Import modules
import numpy as np
import pytest

# Import from package
import seagull as sg
from seagull import lifeforms as lf
from seagull.rules import conway_classic


# Define all rules here
all_rules = [("conway_classic", sg.rules.conway_classic)]


@pytest.mark.parametrize("rule_name, fn", all_rules)
def test_rule_return_shape(rule_name, fn):
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    new_state = fn(board.state)
    assert new_state.shape == (10, 10)


@pytest.mark.parametrize("rule_name, fn", all_rules)
def test_rule_return_type(rule_name, fn):
    board = sg.Board(size=(10, 10))
    board.add(lf.Blinker(length=3), loc=(0, 1))
    new_state = fn(board.state)
    assert isinstance(new_state, (list, np.ndarray))


def test_conway_alive_cell_with_no_neighbor_dies():
    cell = (1, 1)
    state = put_cells_to_board([cell])
    next_state = conway_classic(state)
    assert next_state[cell] == 0


def test_conway_alive_cell_with_one_neighbor_dies():
    cell = (1, 1)
    state = put_cells_to_board([(1, 1), cell])
    next_state = conway_classic(state)
    assert next_state[cell] == 0


def test_conway_alive_cell_with_more_than_3_neighbors_dies():
    cell = (1, 1)
    alive_cells = [(0, 0), (1, 0), (2, 0), (2, 1)]
    state = put_cells_to_board(alive_cells + [cell])
    next_state = conway_classic(state)
    assert next_state[cell] == 0


def test_conway_alive_cell_with_2_neighbors_lives():
    cell = (1, 1)
    alive_cells = [(0, 1), (1, 0)]
    state = put_cells_to_board(alive_cells + [cell])
    next_state = conway_classic(state)
    assert next_state[cell] == 1


def test_conway_alive_cell_with_3_neighbors_lives():
    cell = (1, 1)
    alive_cells = [(0, 0), (1, 0), (2, 1)]
    state = put_cells_to_board(alive_cells + [cell])
    next_state = conway_classic(state)
    assert next_state[cell] == 1


def test_conway_dead_cell_with_three_live_neighbors_lives():
    dead_cell = (1, 1)
    alive_cells = [(2, 2), (1, 0), (2, 1)]
    state = put_cells_to_board(alive_cells)
    next_state = conway_classic(state)
    assert next_state[dead_cell] == 1


def test_conway_dead_cell_with_two_live_neighbors_stay_dead():
    dead_cell = (1, 1)
    alive_cells = [(2, 2), (1, 0)]
    state = put_cells_to_board(alive_cells)
    next_state = conway_classic(state)
    assert next_state[dead_cell] == 0


def put_cells_to_board(coords: List[Tuple[int, int]]) -> np.ndarray:
    """Given a list of cells and their coords, add to board"""
    board = np.zeros((3, 3))
    for coord in coords:
        board[coord] = 1
    return board
