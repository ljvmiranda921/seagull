# -*- coding: utf-8 -*-
"""

utils for LifeForm, original intent - parse .cells and .rle files

Created 20200525 by ep (eugen.pt@gmail.com)
"""

import numpy as np
import urllib
from os.path import isfile

from .base import Lifeform
from .custom import Custom


def parse_plaintext_layout(plaintext_str: str) -> np.ndarray:
    """Parses plaintext_str in Plaintext format into layoutndarray
    
    typical plaintext_str format:
    '''
    .O.O
    O.O
    O
    ......O
    '''

    """
    if type(plaintext_str) == list:
        # already line-split
        lines = plaintext_str
    else:
        # split lines, ignore comments
        lines = plaintext_str.strip().replace("\r\n", "\n").split("\n")
        lines = [line for line in lines if line[0] != "!"]

    # @TODO:check if only '.' and 'O' are present
    layout = [[1 if c == "O" else 0 for c in line] for line in lines]

    max_width = max(len(line) for line in layout)
    # add zeroes so that all lines are of equal length
    [line.extend([0] * (max_width - len(line))) for line in layout]

    return np.array(layout)


def parse_cells(cells_str: str) -> Lifeform:
    """Parses cell_str, stored in Plaintext format, into Lifeform
    
    sample usage:
    G = parse_cells('http://www.conwaylife.com/patterns/glider.cells')
    or
    G = parse_cells('''
            !Name: name of the Lifeform
            ! some comment
            .O
            ..O
            OOO
            '''
        )
    
    . (dot) for empty cell, O (capital O) for alive cell, no trailing .s

    Plaintext format description: https://conwaylife.com/wiki/Plaintext

    Parameters
    ----------
    cells_str : str, also may be a filename or a URL to be (down)loaded from        

    Raises
    ------
    ValueError
        if invalid input provided


    """
    if cells_str[0] not in {".", "0", "!"}:
        # not a proper .cells line, filename?
        if isfile(cells_str):
            print(f"reading from file [{cells_str}]..", end="")
            with open(cells_str, "r") as f:
                cells_str = f.read()
            print("ok")
        elif cells_str[:3] in {"ftp", "htt"}:
            # web-hosted file?
            print(f"trying to download [{cells_str}]..", end="")
            req = urllib.request.urlopen(cells_str)
            if req.getcode() != 200:
                raise ValueError(
                    "Invalid input cells_str,"
                    f" request returned {req.getcode()}"
                )
            print("ok")
            cells_str = req.read().decode("utf-8")
        else:
            raise ValueError("Invalid input cells_str")
    # split lines, \r if (down)loaded and not copy-pasted
    lines = cells_str.strip().replace("\r\n", "\n").split("\n")

    comments = []
    layout = []
    name = None
    author = None
    for line in lines:
        if line and line[0] == "!":
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

    R = Custom(layout)  # LifeForm to be returned

    # Setting custom fields parsed from comments
    R.comments = comments
    if name is not None:
        R.name = name
    if author is not None:
        R.author = author

    return R
