# -*- coding: utf-8 -*-
"""

Functions for parsing LifeForm from Wiki

Created 20200525 by ep (eugen.pt@gmail.com)
"""

# Import standard library
from os.path import isfile
from typing import Union
from urllib.parse import urlparse
from urllib.request import urlopen

# Import modules
import numpy as np
from loguru import logger

from .base import Lifeform
from .custom import Custom


def parse_plaintext_layout(plaintext_str: Union[str, list]) -> np.ndarray:
    """Parse plaintext_str in Plaintext format into ndarray layout

    typical plaintext_str format:
    '''
    .O.O
    O.O
    O
    ......O
    '''

    Parameters
    ----------
    cells_str : Union[str, list]
        Plaintext format lifeform description
        May be a list of lines in which case no comment lines are allowed 

    Raises
    ------
    ValueError
        if invalid input provided

    """
    if isinstance(plaintext_str, list):
        # already line-split
        lines = plaintext_str
    else:
        # split lines, ignore comments
        lines = plaintext_str.strip().replace("\r\n", "\n").split("\n")
        lines = [line for line in lines if line[0] != "!"]

    # @TODO:check if only '.' and 'O' are present
    if set(''.join(lines)) != {'.','O'}:
        raise ValueError("Invalid input cells_str : use only '.' and 'O'")

    layout = [[1 if c == "O" else 0 for c in line] for line in lines]

    max_width = max(len(line) for line in layout)
    # add zeroes so that all lines are of equal length
    [line.extend([0] * (max_width - len(line))) for line in layout]

    return np.array(layout)


def parse_cells(cells_str: str) -> Lifeform:
    """Parse cell_str, stored in Plaintext format, into Lifeform
    
    Plaintext format description: https://conwaylife.com/wiki/Plaintext

    Usage
    -----
    You can enter a string directly into the function: 

    G = parse_cells(
        '''!Name: name of the Lifeform
! some comment
.O
..O
OOO
'''
        )
    # . (dot) for empty cell, O (capital O) for alive cell, no trailing .s

    Or you can parse cells immediately from Conway Life's website:

    G = parse_cells('http://www.conwaylife.com/patterns/glider.cells')
    

    Parameters
    ----------
    cells_str : str
        Plaintext format lifeform description
        May be a filename or a URL to be (down)loaded from        

    Raises
    ------
    ValueError
        if invalid input provided


    """
    if cells_str[0] not in {".", "0", "!"}:
        # not a proper .cells line, filename?
        if isfile(cells_str):
            logger.trace(f"reading from file [{cells_str}]..", end="")
            with open(cells_str, "r") as f:
                cells_str = f.read()
            logger.trace("ok")
        elif urlparse(cells_str).scheme in {"ftp", "http", "https"}:
            # web-hosted file?
            logger.trace(f"trying to download [{cells_str}]..", end="")
            req = urlopen(cells_str)
            if req.getcode() != 200:
                raise ValueError(
                    "Invalid input URL cells_str,"
                    f" request returned {req.getcode()}"
                )
            logger.trace("ok")
            cells_str = req.read().decode("utf-8")
        else:
            raise ValueError("Unrecognized input cells_str")
    # split lines, \r if (down)loaded and not copy-pasted
    lines = cells_str.strip().replace("\r\n", "\n").split("\n")

    comments = []
    layout = []
    name = None
    author = None
    for line in lines:
        if line and line.startswith("!"):
            # parsing commented lines
            # @TODO: prettify? or delete this todo
            if line.startswith("!Name: "):
                name = line[len("!Name: ") :]
            elif line.startswith("!Author: "):
                author = line[len("!Author: ") :]
            else:
                comments.append(line[1:])
        else:
            # collecting layout
            layout.append(line)

    comments = "\n".join(comments)

    layout = parse_plaintext_layout(layout)

    lifeform = Custom(layout)  # to be returned

    # Setting custom fields parsed from comments
    lifeform.comments = comments
    if name is not None:
        lifeform.name = name
    if author is not None:
        lifeform.author = author

    return lifeform
