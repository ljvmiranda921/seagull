# Seagull

A Python library for Conway's Game of Life

This framework allows you to create and simulate various artificial lifeforms
and cellular automatons easily: simply define your board, add your lifeforms,
and execute the `run()` command! It also provides a myriad of pre-made
lifeforms while allowing you to create your custom ones.

**Why name it Seagull?** Conway's Game of Life is quite a mouthful, so I just refer to
its acronym, CGoL. The word "seagull" is just a pun of that.

Simulate your first artificial life in less than 10 lines of code:

```python
import seagull as sg
from seagull.lifeforms import Blinker

board = sg.Board(size=(10,10))
board.add(Blinker(length=3), loc=(4,4))

sim = sg.Simulator(board)
sim.run(sg.rules.conway_classic, iters=1000)
sim.animate()  
```

We have a nice collection of lifeforms for you to choose from!

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
* The `lifeforms` that will interact with the environment, and  
* The `rules` that will dictate if a particular cell will survive or not

In Seagull, you simply define your board, add your lifeforms, and run the
simulation given a rule. You can add multiple lifeforms as you want:

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
hist = sim.run(sg.rules_conway_classic, iters=1000)  # Save simulation history
sim.animate()
```

### Adding custom lifeforms

You can manually create your lifeforms by using the `Custom` class:

```python
import seagull as sg
from seagull.lifeforms import Custom

board = sg.Board(size=(30,30))
board.add(Custom([[0,1,1,0], [0,0,1,1]]))
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

