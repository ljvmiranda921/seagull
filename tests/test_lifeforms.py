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
from seagull.lifeforms.wiki import parse_cells, parse_plaintext_layout, parse_rle, rle2cells, cells2rle

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
    layout = parse_plaintext_layout(['..O','.O','O'])
    assert len(layout.shape) == 2
    assert layout.shape == (3, 3)
    assert np.sum(layout - [[0, 0, 1], [0, 1, 0], [1, 0, 0]]) == 0

def test_parse_plaintext_layout_letters_error():
    """Test if parse_plaintext_layout checks proper letter in input"""
    with pytest.raises(ValueError):
        parse_plaintext_layout(['..O','.OX','O'])

@pytest.mark.skip
def test_glider_lifeform(lifeform):
    """Test if lifeform is a proper Glider"""
    assert len(lifeform.size) == 2
    assert lifeform.size == (3, 3)
    assert np.sum(lifeform.layout - [[0, 1, 0], [0, 0, 1], [1, 1, 1]]) == 0
    assert lifeform.meta['name'] == "Glider"
    assert lifeform.meta['author'] == "Richard K. Guy"


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
    p.write("""!Name: Glider
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
    cells_str = '''.......................OO........................OO
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
....O...................OO'''
    assert rle2cells(cells2rle(cells_str) + '!') == cells_str
