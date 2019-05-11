# -*- coding: utf-8 -*-

"""Lifeforms represent the evolving patterns whenever a rule is applied. In
Seagull, lifeforms are first-class citizens: you can add them to the board,
view them independently, compose, customize, and the like. This library
provides a collection of pre-made lifeforms that you can play around.

Lifeforms are arranged into categories based on their configurations (excluding the Base and Custom lifeforms):


.. autosummary::
    seagull.lifeforms.gliders
    seagull.lifeforms.growers
    seagull.lifeforms.oscillators
    seagull.lifeforms.random
    seagull.lifeforms.static


"""

from .static import Box, Seed, Moon, Kite
from .oscillators import Blinker, Toad, Pulsar
from .gliders import Glider
from .growers import Unbounded
from .random import RandomBox
from .custom import Custom

__all__ = [
    "Box",
    "Seed",
    "Moon",
    "Kite",
    "Blinker",
    "Toad",
    "Pulsar",
    "Glider",
    "Unbounded",
    "RandomBox",
    "Custom",
]
