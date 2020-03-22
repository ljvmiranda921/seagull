# Import standard library
from math import sqrt
from typing import Tuple

# Import modules
import matplotlib.pyplot as plt
import numpy as np
import seagull as sg
import seagull.lifeforms as lf
import streamlit as st
from loguru import logger
from scipy.signal import convolve2d
from palettable import matplotlib as mpl_color
from palettable import scientific


def main():
    # Sidebar
    st.sidebar.header("Parameters")
    st.sidebar.markdown("Control the automata's behavior")
    repro_rate = st.sidebar.slider(
        "Inverse Reproduction rate", min_value=0, max_value=8, value=2
    )
    stasis_rate = st.sidebar.slider(
        "Stasis rate", min_value=0, max_value=8, value=3
    )
    n_iters = st.sidebar.slider(
        "No. of iterations", min_value=0, max_value=20, value=1
    )

    st.sidebar.header("Styling")
    st.sidebar.markdown("Add design and make it unique!")
    n_sprites = st.sidebar.radio(
        "Number of sprites (grid)", options=[1, 4, 9, 16], index=2
    )
    if n_sprites == 1:
        st.sidebar.text("Only applicable for single sprites")
        fill_color = st.sidebar.text_input("Fill color", "#FFFFFF")
        base_color = st.sidebar.text_input("Base color", "#000000")
        colors = [{"fill": fill_color, "base": base_color}]
        try:
            hex_to_rgb(colors[0]["fill"])
            hex_to_rgb(colors[0]["fill"])
        except Exception as e:
            st.exception(ValueError("Cannot convert hex code"))
    else:
        color_schemes = {
            "Inferno": mpl_color.Inferno_20,
            "Viridis": mpl_color.Viridis_20,
            "Magma": mpl_color.Magma_20,
            "Plasma": mpl_color.Plasma_20,
            "Acton": scientific.sequential.Acton_20,
            "Bamako": scientific.sequential.Bamako_20,
            "Batlow": scientific.sequential.Batlow_20,
            "Buda": scientific.sequential.Buda_20,
        }
        scheme = st.sidebar.selectbox("Color scheme", list(color_schemes.keys()))
        hex_colors = color_schemes[scheme].hex_colors
        colors = [
            {"fill": fill, "base": base}
            for fill, base in zip(hex_colors, hex_colors[::-1])
        ]

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
                colors=colors,
            )
    else:
        with st.spinner("Wait for it..."):
            fig = make_sprite(
                n_sprites=n_sprites,
                n_iters=n_iters,
                repro_rate=repro_rate,
                stasis_rate=stasis_rate,
                colors=colors,
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
    colors=None,
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
    colors: list of dicts
        Must have keys for `fill` and `base`

    """
    logger.info("Initializing board")
    board = sg.Board(size=(8, 4))

    logger.info("Running simulation")
    sprator_list = []

    for i, color in zip(range(n_sprites), colors):
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

        logger.info(f"Generating sprite/s: {i}")
        sprator = np.hstack([fstate, np.fliplr(fstate)])
        sprator = np.pad(
            sprator, mode="constant", pad_width=1, constant_values=1
        )
        sprator_colored = apply_color(sprator, color["fill"], color["base"])
        sprator_list.append(sprator_colored)

    # Generate plot based on the grid size
    n_grid = int(sqrt(n_sprites))

    if n_grid == 1:
        fig, axs = plt.subplots(n_grid, n_grid, figsize=(5, 5))
        axs = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)
        axs.imshow(sprator_list[0], interpolation="nearest")
        fig.text(0, -0.05, "bit.ly/CellularSprites", ha="left", color="black")
    else:
        fig, axs = plt.subplots(n_grid, n_grid, figsize=(5, 5))
        for ax, sprator in zip(axs.flat, sprator_list):
            ax.imshow(sprator, interpolation="nearest")
            ax.set_axis_off()
        fig.text(0.125, 0.05, "bit.ly/CellularSprites", ha="left")

    return fig


def custom_rule(X, repro_rate=3, stasis_rate=3) -> np.ndarray:
    """Custom Sprator Rule"""
    n = convolve2d(X, np.ones((3, 3)), mode="same", boundary="fill") - X
    reproduction_rule = (X == 0) & (n <= repro_rate)
    stasis_rule = (X == 1) & ((n == 2) | (n == stasis_rate))
    return reproduction_rule | stasis_rule


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    """Convert a hex code to an RGB tuple"""
    h_ = h.lstrip("#")
    rgb = tuple(int(h_[i : i + 2], 16) for i in (0, 2, 4))
    return rgb


def apply_color(
    sprite: np.ndarray, fill_color: str, base_color: str
) -> np.ndarray:
    """Apply color to the sprite"""
    sprite_color = [
        (sprite * base) + (np.invert(sprite) * fill)
        for base, fill in zip(hex_to_rgb(base_color), hex_to_rgb(fill_color))
    ]
    return np.rollaxis(np.asarray(sprite_color), 0, 3)


main()
