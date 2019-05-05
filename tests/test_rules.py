# -*- coding: utf-8 -*-

# Import standard library
from inspect import getmembers, isfunction

# Import modules
import numpy as np
import pytest

# Import from package
import seagull as sg
from seagull import lifeforms as lf

all_rules = [r for r in getmembers(sg.rules) if isfunction(r[1])]


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
