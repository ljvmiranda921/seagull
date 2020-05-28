# Import standard library
import random
from math import sqrt
from typing import Tuple

# Import modules
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import seagull as sg
import seagull.lifeforms as lf
import streamlit as st
from loguru import logger
from scipy.signal import convolve2d


def main():
    # Sidebar
    st.sidebar.header("Parameters")
    st.sidebar.markdown("Control the automata's behavior")
    repro_rate = st.sidebar.slider(
        "Extinction rate: controls how many dead cells will stay dead on the next iteration",
        min_value=0,
        max_value=8,
        value=2,
    )
    stasis_rate = st.sidebar.slider(
        "Stasis rate: controls how many live cells will stay alive on the next iteration",
        min_value=0,
        max_value=8,
        value=3,
    )
    n_iters = st.sidebar.slider(
        "No. of iterations", min_value=0, max_value=20, value=1
    )

    st.sidebar.header("Styling")
    st.sidebar.markdown("Add design and make it unique!")
    n_sprites = st.sidebar.radio(
        "Number of sprites (grid)", options=[1, 4, 9, 16], index=2
    )

    # Main Page
    st.title("Create sprites using Cellular Automata!")
    st.markdown(
        """
        ## Instructions

        Play with the parameters in the sidebar to generate your own 8-bit sprites.
    """
    )

    if st.button("Refresh"):
        with st.spinner("Wait for it..."):
            fig = make_sprite(
                n_sprites=n_sprites,
                n_iters=n_iters,
                repro_rate=repro_rate,
                stasis_rate=stasis_rate,
            )
    else:
        with st.spinner("Wait for it..."):
            fig = make_sprite(
                n_sprites=n_sprites,
                n_iters=n_iters,
                repro_rate=repro_rate,
                stasis_rate=stasis_rate,
            )

    st.pyplot(fig=fig, bbox_inches="tight")

    st.markdown("*To download, simply right-click the image, and save as PNG*")

    st.markdown(
        """

        ## Cellular Automata?

        **Cellular Automata** is an abstract computational system that evolves
        given a discrete number of steps and a set of rules governing its
        behaviour. The classic Conway's Game of Life has the following rules:
        * **Overpopulation**: if a living cell is surrounded by more that three
        living cells, it dies.
        * **Stasis**: if a living cell is surrounded by two or three living cells,
        it survives.
        * **Underpopulation**: if a living cell is surrounded by fewer than two
        living cells, it dies
        * **Reproduction**: if a dead cell is surrounded by exactly three cells, it
        becomes a live cell.

        I find artifical life and nature-inspired computing highly-interesting.
        Before, I made a particle swarm optimization library called
        [PySwarms](https://github.com/ljvmiranda921/pyswarms), then two years
        later, I built a Conways' Game of Life simulator called
        [Seagull](https://github.com/ljvmiranda921/seagull). There's a certain
        energy and curiosity whenever I see these simulations seemingly "come
        to life!"

        ## Contributing

        Contributions are welcome! The source code for this web app can be found
        [here](https://github.com/ljvmiranda921/seagull/tree/master/docs/notebooks).
        For Issues and Pull Requests, please direct them to this [link](https://github.com/ljvmiranda921/seagull/issues)!

    """
    )

    st.markdown(
        """
        ---
        This application is made with :heart: by [Lj V.
        Miranda](ljvmiranda921.github.io) using
        [ljvmiranda921/seagull](https://github.com/ljvmiranda921/seagull), a
        Python library for Conway's Game of Life, and
        [Streamlit](https://github.com/streamlit/streamlit)! Inspired and
        ported into Python from
        [yurkth/sprator](https://github.com/yurkth/sprator).
    """
    )


def make_sprite(
    n_sprites: int,
    n_iters: int,
    repro_rate: int,
    stasis_rate: int,
):
    """Main function for creating sprites

    Parameters
    ----------
    n_sprites : int
        Number of sprites to generate
    n_iters : int
        Number of iterations to run the simulator
    repro_rate : int
        Inverse reproduction rate
    stasis_rate : int
        Stasis rate
    """
    logger.info("Initializing board")
    board = sg.Board(size=(8, 4))

    logger.info("Running simulation")
    sprator_list = []

    for sprite in range(n_sprites):
        noise = np.random.choice([0, 1], size=(8, 4))
        custom_lf = lf.Custom(noise)
        board.add(custom_lf, loc=(0, 0))
        sim = sg.Simulator(board)
        sim.run(
            custom_rule,
            iters=n_iters,
            repro_rate=repro_rate,
            stasis_rate=stasis_rate,
        )
        fstate = sim.get_history()[-1]

        logger.info(f"Generating sprite/s: {sprite}")
        sprator = np.hstack([fstate, np.fliplr(fstate)])
        sprator = np.pad(
            sprator, mode="constant", pad_width=1, constant_values=1
        )
        sprator_with_outline = add_outline(sprator)
        sprator_gradient = get_gradient(sprator_with_outline)
        sprator_final = combine(sprator_with_outline, sprator_gradient)
        sprator_list.append(sprator_final)

    # Generate plot based on the grid size
    n_grid = int(sqrt(n_sprites))

    # Generate random colors as cmap
    r = lambda: "#%02X%02X%02X" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    colors = ["black", "#f2f2f2", r(), r(), r()]
    cm.register_cmap(
        cmap=mpl.colors.LinearSegmentedColormap.from_list(
            "custom", colors
        ).reversed()
    )

    if n_grid == 1:
        fig, axs = plt.subplots(n_grid, n_grid, figsize=(5, 5))
        axs = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
        axs.imshow(sprator_list[0], cmap="custom_r", interpolation="nearest")
        fig.text(0, -0.05, "bit.ly/CellularSprites", ha="left", color="black")
    else:
        fig, axs = plt.subplots(n_grid, n_grid, figsize=(5, 5))
        for ax, sprator in zip(axs.flat, sprator_list):
            # TODO: Remove duplicates
            # Generate random colors as cmap
            r = lambda: "#%02X%02X%02X" % (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            colors = ["black", "#f2f2f2", r(), r(), r()]
            cm.register_cmap(
                cmap=mpl.colors.LinearSegmentedColormap.from_list(
                    "custom", colors
                ).reversed()
            )
            ax.imshow(sprator, cmap="custom_r", interpolation="nearest")
            ax.set_axis_off()
        fig.text(0.125, 0.05, "bit.ly/CellularSprites", ha="left")

    return fig


def custom_rule(X, repro_rate=3, stasis_rate=3) -> np.ndarray:
    """Custom Sprator Rule"""
    n = convolve2d(X, np.ones((3, 3)), mode="same", boundary="fill") - X
    reproduction_rule = (X == 0) & (n <= repro_rate)
    stasis_rule = (X == 1) & ((n == 2) | (n == stasis_rate))
    return reproduction_rule | stasis_rule


def add_outline(mat: np.ndarray) -> np.ndarray:
    """Pad the matrix"""
    m = np.ones(mat.shape)
    for idx, orig_val in np.ndenumerate(mat):
        x, y = idx
        neighbors = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        if orig_val == 0:
            m[idx] = 0  # Set the coordinate in the new matrix as 0
            for n_coord in neighbors:
                try:
                    m[n_coord] = 0.5 if mat[n_coord] == 1 else 0
                except IndexError:
                    pass

    m = np.pad(m, mode="constant", pad_width=1, constant_values=1)
    # Let's do a switcheroo, I know this isn't elegant but please feel free to
    # do a PR to make this more efficient!
    m[m == 1] = np.inf
    m[m == 0.5] = 1
    m[m == np.inf] = 0.5

    return m


def get_gradient(mat: np.ndarray) -> np.ndarray:
    """Get gradient of an outline sprator"""
    grad = np.gradient(mat)[0]

    def _remap(new_range, matrix):
        old_min, old_max = np.min(matrix), np.max(matrix)
        new_min, new_max = new_range
        old = old_max - old_min
        new = new_max - new_min
        return (((matrix - old_min) * new) / old) + new_min

    return _remap((0.2, 0.25), grad)


def combine(mat_outline: np.ndarray, mat_gradient: np.ndarray):
    """Combine the matrix with outline and the one with grads"""
    mat_final = np.copy(mat_outline)
    mask = mat_outline == 0
    mat_final[mask] = mat_gradient[mask]
    return mat_final


main()
