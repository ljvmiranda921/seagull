.. Seagull documentation master file, created by
   sphinx-quickstart on Sat May 11 10:32:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Seagull!
===================

.. image:: https://img.shields.io/pypi/v/pyseagull.svg?color=brightgreen&logo=python&logoColor=white
   :target: https://pypi.org/project/pyseagull/
   :alt: PyPI Version

.. image:: https://dev.azure.com/ljvmiranda/ljvmiranda/_apis/build/status/ljvmiranda921.seagull?branchName=master
   :target: https://dev.azure.com/ljvmiranda/ljvmiranda/_build/latest?definitionId=3&branchName=master
   :alt: Build Status

.. image:: https://codecov.io/gh/ljvmiranda921/seagull/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ljvmiranda921/seagull
   :alt: Code Coverage

.. image:: https://img.shields.io/github/license/ljvmiranda921/seagull.svg?color=blue
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT


A Python library for Conway's Game of Life

This framework allows you to create and simulate various artificial lifeforms
and cellular automata easily: simply define your board, add your lifeforms,
and execute the `run` command! It also provides a myriad of pre-made
lifeforms while allowing you to create your own.


**Why name it Seagull?** Conway's Game of Life is quite a mouthful, so I just refer to
its acronym, CGoL. The word "seagull" is just a pun of that.

- **Free Software**: MIT License
- **Github Repository**: https://github.com/ljvmiranda921/seagull

`Conway's Game of Life
<https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>`_ is considered a
zero-player game: you simply set-up your initial configuration on the board and
observe how it evolves through time.

Simulate your first lifeforms in a few lines of code:

.. code-block:: python

   import seagull as sg
   from seagull.lifeforms import Pulsar

   # Initialize board
   board = sg.Board(size=(19,60))  

   # Add three Pulsar lifeforms in various locations
   board.add(Pulsar(), loc=(1,1))
   board.add(Pulsar(), loc=(1,22))
   board.add(Pulsar(), loc=(1,42))

   # Simulate board
   sim = sg.Simulator(board)      
   sim.run(sg.rules.conway_classic, iters=1000)

Optionally, you can animate the simulation by running :code:`sim.animate()`:

.. image::  https://imgur.com/sgCrP9f.gif
   :width: 720


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: General

   installation
   concepts
   examples
   changelog

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Developers

   contributing
   code_of_conduct

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API Documentation

   api/seagull.board
   api/seagull.simulator
   api/seagull.lifeforms
   api/seagull.rules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
