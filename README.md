<p align="center">
    <img src="https://imgur.com/Vgt6a5y.png" width="200">
</p>

<p align="center">
    <a href="https://pypi.org/project/pyseagull/"><img src="https://img.shields.io/pypi/v/pyseagull.svg?color=brightgreen&logo=python&logoColor=white"></img></a>
    <a href="https://dev.azure.com/ljvmiranda/ljvmiranda/_build/latest?definitionId=3&branchName=master"><img src="https://dev.azure.com/ljvmiranda/ljvmiranda/_apis/build/status/ljvmiranda921.seagull?branchName=master"></img></a>
    <a href="https://pyseagull.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/pyseagull/badge/?version=latest"></img></a>
    <a href="https://codecov.io/gh/ljvmiranda921/seagull"><img src="https://codecov.io/gh/ljvmiranda921/seagull/branch/master/graph/badge.svg"></img></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/ljvmiranda921/seagull.svg?color=blue"></img></a>
</p>



A Python library for Conway's Game of Life

This framework allows you to create and simulate various artificial lifeforms
and cellular automata easily: simply define your board, add your lifeforms,
and execute the `run` command! It also provides a myriad of pre-made
lifeforms while allowing you to create your own.

**Why name it Seagull?** Conway's Game of Life is quite a mouthful, so I just refer to
its acronym, CGoL. The word "seagull" is just a pun of that.

Simulate your first lifeforms in few lines of code:

```python
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
```

Optionally, you can animate the simulation by running `sim.animate()`:

<p align="center">
  <img src="https://imgur.com/sgCrP9f.gif" width="720">
</p>

Aside from `Pulsar`, we have a [nice collection of
lifeforms](https://pyseagull.readthedocs.io/en/latest/api/seagull.lifeforms.html)
for you to choose from!

## Installation

To install Seagull, run this command in your terminal:

```shell
pip install pyseagull
```

This is the preferred method to install Seagull, as it will always install
the most recent stable release.

In case you want to install the bleeding-edge version, clone this repo:

```shell
git clone https://github.com/ljvmiranda921/seagull.git
```

and then run

```shell
cd seagull
python setup.py install
```

## Usage

There are three main components for an artificial life simulation:

* The `Board` or the environment in which the lifeforms will move around
* The `Lifeform` that will interact with the environment, and  
* The `rules` that dictate if a particular cell will survive or not

In Seagull, you simply define your `Board`, add your `Lifeform`/s, and run the
`Simulator` given a `rule`. You can add multiple lifeforms as you want:

```python
import seagull as sg
from seagull import lifeforms as lf

board = sg.Board(size=(30,30))
board.add(lf.Blinker(length=3), loc=(4,4))
board.add(lf.Glider(), loc=(10,4))
board.add(lf.Glider(), loc=(15,4))
board.add(lf.Pulsar(), loc=(5,12))
board.view()  # View the current state of the board
```

Then you can simply run the simulation, and animate it when needed:

```python
sim = sg.Simulator(board)
hist = sim.run(sg.rules.conway_classic, iters=1000)  # Save simulation history
sim.animate()
```

### Adding custom lifeforms

You can manually create your lifeforms by using the `Custom` class:

```python
import seagull as sg
from seagull.lifeforms import Custom

board = sg.Board(size=(30,30))
board.add(Custom([[0,1,1,0], [0,0,1,1]]), loc=(0,0))
```

### Obtaining simulation statistics and history 

By default, the simulation statistics will always be returned after calling the
`run()` method. In addition, you can also obtain the history by calling the
`get_history()` method.

```python
# The run() command returns the run statistics
stats = sim.run(sg.rules.conway_classic, iters=1000)
# You can also get it using get_history()
hist = sim.get_history()
```

## Examples

You can find more examples in the
[documentation](https://pyseagull.readthedocs.io/en/latest/examples.html)

## Contributing

This project is open for contributors! Contibutions can come in the form of
feature requests, bug fixes, documentation, tutorials and the like! We highly
recommend to file an Issue first before submitting a [Pull
Request](https://help.github.com/en/articles/creating-a-pull-request).

Simply fork this repository and make a Pull Request! We'd definitely
appreciate:

* Implementation of new features
* Bug Reports
* Documentation
* Testing


## License

MIT License (c) 2019, Lester James V. Miranda

