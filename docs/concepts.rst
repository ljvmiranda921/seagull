Concepts
========

There are three main components for an artificial life simulation:

* The :code:`Board` or the environment in which the lifeforms will move around
* The :code:`Lifeform` that will interact with the environment, and  
* The :code:`rules` that dictate if a particular cell will survive or not

In the classic Conway's Game of Life, there are four rules (taken from
`@jakevdp <https://twitter.com/jakevdp>`_'s blog `post
<https://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/>`_):

* **Overpopulation**: if a living cell is surrounded by more than three living cells, it dies
* **Stasis**: if a living cell is surrounded by two or three living cells, it survives
* **Underpopulation**: if a living cell is surrounded by fewer than two living cells, it dies
* **Reproduction**: if a dead cell is surrounded by exactly three cells, it becomes a live cell

In Seagull, you simply define your :code:`Board`, add your :code:`Lifeform`/s,
and run the :code:`Simulator` given a :code:`rule`. You can add multiple
lifeforms as you want:

.. code-block:: python

   import seagull as sg
   from seagull import lifeforms as lf

   board = sg.Board(size=(30,30))
   board.add(lf.Blinker(length=3), loc=(4,4))
   board.add(lf.Glider(), loc=(10,4))
   board.add(lf.Glider(), loc=(15,4))
   board.add(lf.Pulsar(), loc=(5,12))
   board.view()  # View the current state of the board

Then you can simply run the simulation, and animate it when needed:

.. code-block:: python

   sim = sg.Simulator(board)
   stats = sim.run(sg.rules.conway_classic, iters=1000)
   sim.animate()

Adding custom lifeforms
-----------------------

You can manually create your lifeforms by using the :code:`Custom` class:

.. code-block:: python

   import seagull as sg
   from seagull.lifeforms import Custom

   board = sg.Board(size=(30,30))
   board.add(Custom([[0,1,1,0], [0,0,1,1]]), loc=(0,0))

Obtaining simulation statistics and history 
-------------------------------------------

By default, the simulation statistics will always be returned after calling the
:code:`run()` method. In addition, you can also obtain the history by calling the
:code:`get_history()` method.

.. code-block:: python

   # The run() command returns the run statistics
   stats = sim.run(sg.rules.conway_classic, iters=1000)
   # You can also get it using get_history()
   hist = sim.get_history()

