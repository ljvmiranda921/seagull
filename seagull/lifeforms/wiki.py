# -*- coding: utf-8 -*-
"""
Contains functions for parsing LifeForms directly from `LifeWiki <https://www.conwaylife.com/wiki/Main_Page>`_

LifeWiki contains Pattern files of two kinds: **PlainText  .cells files** and **.rle files**


The `.cells` format
-------------------------

The `.cells` files are LifeForms stored in `Plaintext  <https://conwaylife.com/wiki/Plaintext>`_
format

The `.cells` files are parsed using the :func:`seagull.lifeforms.wiki.parse_cells` function,
which may parse the lifeform from the input str, 
or load it from file if filename/URL is provided as input::

    glider = parse_cells('''!Name: name of the Lifeform
    ! some comment
    .O
    ..O
    OOO
    ''')
    
    glider = parse_cells('~/glider.cells') # download it first!
    
    glider = parse_cells('http://www.conwaylife.com/patterns/glider.cells')

If you only need to parse layout, you may use the underlying :func:`seagull.lifeforms.wiki.parse_plaintext_layout` function::

    layout = parse_plaintext_layout('''!Name: Name
    ! comment
    ..O
    .O
    O
    ''')


>>> layout
array([[0, 0, 1],
       [0, 1, 0],
       [1, 0, 0]])


.rle files
----------

Currently not suppored, working on it!


Created 20200525 by ep (eugen.pt@gmail.com)
"""

# Import standard library
from os.path import isfile
import re
from typing import Dict, List, Union
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
        lines = [line for line in lines if not line.startswith("!")]

    # check if only '.' and 'O' are present
    if set("".join(lines)) != {".", "O"}:
        raise ValueError("Invalid input cells_str : use only '.' and 'O'")

    layout = [[1 if c == "O" else 0 for c in line] for line in lines]

    max_width = max(len(line) for line in layout)
    # add zeroes so that all lines are of equal length
    [line.extend([0] * (max_width - len(line))) for line in layout]

    return np.array(layout)


def _get_metadata(lines: List[str]) -> Dict:
    """Parse meta-data stored in the comments of .cells file

    Args:
        lines (List[str]): comment lines to be parsed

    Returns:
        Dict of meta-data by keys. Curently supported keys:
        - name     : from line starting with "!Name: "
        - author   : from line starting with "!Author: "
        - comments : for all other comments
    """
    meta = {"comments": []}
    for line in lines:
        if line.startswith("!"):
            # parsing commented lines
            # @TODO: prettify? or delete this todo
            if line.startswith("!Name: "):
                meta["name"] = line[len("!Name: ") :]
            elif line.startswith("!Author: "):
                meta["author"] = line[len("!Author: ") :]
            else:
                meta["comments"].append(line[1:])
        elif line.startswith("#"):
            # parsing commented lines
            # @TODO: prettify? or delete this todo
            if line.startswith("#N "):
                meta["name"] = line[len("#N ") :]
            elif line.startswith("#O "):
                meta["author"] = line[len("#O ") :]
            elif line.startswith(("#R ", "#P ", "#r ")):
                # @TODO: decide whether add R, P, r parsing?
                raise NotImplementedError("#R, #r , #P tags not implemented")
            else:
                meta["comments"].append(
                    line[3:]
                )  # 3: for proper "#C <comment>" format
        else:
            # not a comment line
            pass

    meta["comments"] = "\n".join(meta["comments"])

    return meta


def _load_file_of_url(path: str) -> str:
    """Detects if path is local or URL, loads file content

    Args:
        path (str): [description]

    Returns:
        str: [description]
    """
    if isfile(path):
        logger.trace(f"reading from file [{path}]..", end="")
        with open(path, "r") as f:
            content = f.read()
        logger.trace("ok")
    elif urlparse(path).scheme in {"ftp", "http", "https"}:
        logger.trace(f"trying to download [{path}]..", end="")
        req = urlopen(path)
        if req.getcode() != 200:
            raise ValueError(
                f"Invalid input URL request returned {req.getcode()}"
            )
        logger.trace("ok")
        content = req.read().decode("utf-8")
    else:
        raise ValueError(f"Unrecognized input path {path}")

    return content


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
    if not cells_str.startswith((".", "0", "!")):
        # not a proper .cells line, filename/URL?
        cells_str = _load_file_of_url(cells_str)

    # split lines, \r if (down)loaded and not copy-pasted
    lines = cells_str.strip().replace("\r\n", "\n").split("\n")

    metadata_lines = [l for l in lines if l.startswith("!")]
    layout_lines = [l for l in lines if not l.startswith("!")]

    layout = parse_plaintext_layout(layout_lines)

    lifeform = Custom(layout)  # to be returned

    # Setting custom fields parsed from comments
    lifeform.meta = _get_metadata(metadata_lines)

    return lifeform


def cells2rle(cells_str: Union[list, str]) -> str:
    """Convert plaintext coded lifeform into RLE, ignore comments

    Does not add "!" at the end, converts only commands
        (idea behind this is that it insures that you know what you're doing)

    Parameters
    ----------
    cells_str : Union[list, str]
        Plaintext format lifeform description
        may be a list of lines or a str, possibly multiline

    Returns
    -------
    str
        in RLE format, no header, no comments, no trailing "!"
    """
    if isinstance(cells_str, str):
        cells_str = cells_str.replace("\r\n", "\n").split("\n")

    cells_str = "\n".join(l for l in cells_str if not l.startswith("!"))
    blocks = re.findall("(\n+|\\.+|O+)", cells_str)
    parse_dict = {"\n": "$", ".": "b", "O": "o"}
    blocks = [
        (str(len(b)) if len(b) > 1 else "") + parse_dict[b[0]] for b in blocks
    ]

    return "".join(blocks)


def rle2cells(rle_str: str) -> str:
    """Convert lifeform string in RLE encoding to PlainText

    Args:
        rle_str (str): single line of RLE commands

    Returns:
        str: valid PlainText-encoded lifeform
    """
    # drop the last part
    if "!" in rle_str:
        rle_str = rle_str[: rle_str.index("!")]
    else:
        raise ValueError('Incorrect input: no "!"')

    if not set(rle_str).issubset("0123456789bo$"):
        raise ValueError("Incorrect input: wrong character set")

    commands = re.findall("([0-9]*)(b|o|\\$)", rle_str)
    if len(commands) == 0:
        raise ValueError("Incorrect input: wrong pattern format")

    layout_string = ""
    parse_dict = {"b": ".", "o": "O", "$": "\n"}
    for com in commands:
        n = int(com[0]) if com[0] else 1
        layout_string += parse_dict[com[1]] * n

    return layout_string


def parse_rle(rle_str: str) -> Lifeform:
    """Parse rle_str, stored in RLE format, into Lifeform
    
    RLE format description: https://www.conwaylife.com/wiki/Run_Length_Encoded

    Usage
    -----
    You can enter a string directly into the function: 

    G = parse_rle(
        '''#N Gosper glider gun
#O Bill Gosper
#C A true period 30 glider gun.
#C The first known gun and the first known finite pattern with unbounded growth.
#C www.conwaylife.com/wiki/index.php?title=Gosper_glider_gun
x = 36, y = 9, rule = B3/S23
24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8b
o3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!
'''
        )
    
    Or you can parse rle files immediately from Conway Life's website:

    G = parse_rle('http://www.conwaylife.com/patterns/gosperglidergun.rle')


    Parameters
    ----------
    rle_str : str
        RLE encoded lifeform description
        May be a filename or a URL to be (down)loaded from        

    Raises
    ------
    ValueError
        if invalid input provided

    Notes
    -----
        - RLE content after `!` is ignored    
        - header line is currently parsed but not used
    """
    if not rle_str.startswith(("#", "x")):
        # not a proper .cells line, filename/URL?
        rle_str = _load_file_of_url(rle_str)

    # split lines, \r if (down)loaded and not copy-pasted
    lines = rle_str.strip().replace("\r\n", "\n").split("\n")

    metadata_lines = [l for l in lines if l.startswith("#")]
    layout_lines = [l for l in lines if not l.startswith("#")]

    # Parse size and rule, if present
    header_line = layout_lines[0]
    header_match = re.match(
        r"x = ([0-9]+), y = ([0-9]+)(, rule = ([^ ]+))?", header_line
    )
    if header_match is None:
        raise ValueError(
            f"Incorrect input: wrong header line format : [{header_line}]"
        )
    header_match = header_match.groups()

    width = int(header_match[0])
    height = int(header_match[1])

    if header_match[3] is None:
        # use default rulestring
        rulestring = "B3/S23"
    else:
        rulestring = header_match[3]

    # Parse layout, converting it to plaintext
    layout_string = "".join(layout_lines[1:])
    layout_string = rle2cells(layout_string)
    layout = parse_plaintext_layout(layout_string)

    if layout.shape != (height, width):
        raise ValueError(
                'Parsed layout width/height inconsistent with header'
                f': header: {width} {height} , layout: {layout.shape}'
            )

    lifeform = Custom(layout)  # to be returned

    # Setting custom fields parsed from comments
    lifeform.meta = _get_metadata(metadata_lines)

    return lifeform
