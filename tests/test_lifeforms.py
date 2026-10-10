# -*- coding: utf-8 -*-

# Import standard library
from inspect import getmembers, isclass

# Import modules
import numpy as np
import pytest
from matplotlib.figure import Figure
from matplotlib.image import AxesImage

# Import from package
import seagull as sg
from seagull.lifeforms.wiki import (
    parse_cells,
    parse_plaintext_layout,
    parse_rle,
    rle2cells,
    cells2rle,
)


def _place_on_board(layout, size):
    """Center a lifeform layout on an empty square board of the given size.

    The rules in this module count neighbours with a wrap-around boundary, so
    the board has to be large enough for the pattern to never touch an edge.
    """
    X = np.zeros((size, size))
    h, w = layout.shape
    r0, c0 = (size - h) // 2, (size - w) // 2
    X[r0 : r0 + h, c0 : c0 + w] = layout
    return X


def _live_cells(X):
    return {
        (r, c) for r in range(X.shape[0]) for c in range(X.shape[1]) if X[r, c]
    }


all_lifeforms = [
    lf
    for lf in getmembers(sg.lifeforms)
    if isclass(lf[1]) and lf[0] != "Custom"
]


@pytest.mark.parametrize("lifeform, cls", all_lifeforms)
def test_lifeform_size(lifeform, cls):
    """Test if getting the lifeform size returns a tuple of size 2"""
    assert len(cls().size) == 2


@pytest.mark.parametrize("lifeform, cls", all_lifeforms)
def test_lifeform_layout(lifeform, cls):
    """Test if getting the lifeform layout returns a numpy array"""
    assert isinstance(cls().layout, np.ndarray)
    assert len(cls().layout.shape) == 2


@pytest.mark.parametrize("lifeform, cls", all_lifeforms)
def test_lifeform_view(lifeform, cls):
    """Test if getting the lifeform view returns the expected tuple"""
    result = cls().view()
    assert len(result) == 2
    assert isinstance(result[0], Figure)
    assert isinstance(result[1], AxesImage)


def test_custom_validate_input_values():
    """Test if error is raised when input array is not binary"""
    with pytest.raises(ValueError):
        sg.lifeforms.Custom(np.random.uniform(size=(3, 3)))


def test_custom_validate_input_shape():
    """Test if error is raised when input array has wrong dimensions"""
    with pytest.raises(ValueError):
        sg.lifeforms.Custom(np.random.choice([0, 1], size=(1, 3, 3)))


def test_parse_plaintext_layout():
    """Test if parse_plaintext_layout parses sample text correctly"""
    layout = parse_plaintext_layout(
        """!Name: Name
! comment
..O
.O
O
"""
    )
    assert len(layout.shape) == 2
    assert layout.shape == (3, 3)
    assert np.sum(layout - [[0, 0, 1], [0, 1, 0], [1, 0, 0]]) == 0


def test_parse_plaintext_layout_list():
    """Test if parse_plaintext_layout parses sample list input correctly"""
    layout = parse_plaintext_layout(["..O", ".O", "O"])
    assert len(layout.shape) == 2
    assert layout.shape == (3, 3)
    assert np.sum(layout - [[0, 0, 1], [0, 1, 0], [1, 0, 0]]) == 0


def test_parse_plaintext_layout_letters_error():
    """Test if parse_plaintext_layout checks proper letter in input"""
    with pytest.raises(ValueError):
        parse_plaintext_layout(["..O", ".OX", "O"])


@pytest.mark.skip
def test_glider_lifeform(lifeform):
    """Test if lifeform is a proper Glider"""
    assert len(lifeform.size) == 2
    assert lifeform.size == (3, 3)
    assert np.sum(lifeform.layout - [[0, 1, 0], [0, 0, 1], [1, 1, 1]]) == 0
    assert lifeform.meta["name"] == "Glider"
    assert lifeform.meta["author"] == "Richard K. Guy"


def test_lifeform_parse_cells():
    """Test if lifeform is properly parsed from text"""
    lifeform = parse_cells(
        """!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
.O
..O
OOO"""
    )
    test_glider_lifeform(lifeform)


def test_lifeform_parse_cells_file(tmpdir):
    """Test if lifeform is properly parsed from file"""
    p = tmpdir.mkdir("sub").join("glider.cells")
    p.write(
        """!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
.O
..O
OOO"""
    )
    lifeform = parse_cells(str(p))
    test_glider_lifeform(lifeform)


def test_lifeform_parse_cells_url():
    """Test if lifeform is properly parsed from URL"""
    lifeform = parse_cells("http://www.conwaylife.com/patterns/glider.cells")
    test_glider_lifeform(lifeform)


def test_lifeform_parse_rle():
    """Test if lifeform is properly parsed from rle-encoded text"""
    lifeform = parse_rle(
        """#N Glider
#O Richard K. Guy
#C The smallest, most common, and first discovered spaceship.
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3
bo$2bo$3o!"""
    )
    test_glider_lifeform(lifeform)


def test_lifeform_cells2rle():
    """Test of cells2rle conversion, relies on rle2cells being OK"""
    cells_str = """.......................OO........................OO
.......................OO........................OO
.........................................OO
........................................O..O
.........................................OO

....................................OOO
....................................O.O
.........OO.........................OOO
.........OO.........................OO
........O..O.......................OOO
........O..O.OO....................O.O
........O....OO....................OOO
..........OO.OO
...............................OO
.....................OO.......O..O
.....................OO........OO
.................................................OO
.................................................OO

....OO..................O
OO....OOOO..........OO..OO.OOO
OO..OO.OOO..........OO....OOOO
....O...................OO"""
    assert rle2cells(cells2rle(cells_str) + "!") == cells_str


def test_heavyweight_spaceship_is_a_period_4_c2_spaceship():
    """The HWSS travels 2 cells every 4 generations, population unchanged"""
    lifeform = sg.lifeforms.HeavyweightSpaceship()
    board = _place_on_board(lifeform.layout, size=60)
    before = _live_cells(board)
    for _ in range(8):  # two full periods
        board = sg.rules.conway_classic(board)
    after = _live_cells(board)
    assert len(before) == 13
    # c/2 means two cells per period, so eight generations shift it by four
    assert after == {(r, c - 4) for r, c in before}


def test_heavyweight_spaceship_shifts_two_cells_per_period():
    """One period (4 generations) translates the ship by exactly two cells"""
    lifeform = sg.lifeforms.HeavyweightSpaceship()
    board = _place_on_board(lifeform.layout, size=60)
    before = _live_cells(board)
    for _ in range(4):
        board = sg.rules.conway_classic(board)
    after = _live_cells(board)
    assert len(after) == 13
    assert after == {(r, c - 2) for r, c in before}
    assert after != before  # it actually moved


def test_diehard_disappears_after_exactly_130_generations():
    """Diehard vanishes at generation 130 and not a single generation sooner"""
    lifeform = sg.lifeforms.Diehard()
    board = _place_on_board(lifeform.layout, size=100)
    for generation in range(1, 130):
        board = sg.rules.conway_classic(board)
        assert np.sum(board) > 0, "died early at generation %d" % generation
    board = sg.rules.conway_classic(board)
    assert np.sum(board) == 0, "still alive after 130 generations"


def test_acorn_grows_before_stabilizing():
    """Acorn takes 5206 generations to settle, its growth is pinned here"""
    lifeform = sg.lifeforms.Acorn()
    board = _place_on_board(lifeform.layout, size=100)
    populations = {}
    for generation in range(1, 51):
        board = sg.rules.conway_classic(board)
        if generation in (1, 2, 4, 8, 50):
            populations[generation] = int(np.sum(board))
    assert populations == {1: 8, 2: 10, 4: 11, 8: 18, 50: 96}


def test_rpentomino_grows_before_stabilizing():
    """The R-pentomino takes 1103 generations to settle, growth pinned here"""
    lifeform = sg.lifeforms.Rpentomino()
    board = _place_on_board(lifeform.layout, size=100)
    populations = {}
    for generation in range(1, 51):
        board = sg.rules.conway_classic(board)
        if generation in (1, 2, 4, 8, 50):
            populations[generation] = int(np.sum(board))
    assert populations == {1: 6, 2: 7, 4: 8, 8: 18, 50: 64}
