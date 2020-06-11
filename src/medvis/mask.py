"""Tools for overlaying segmentation masks onto medical images.
"""


__author__ = "Yngve Mardal Moe"


import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.ndimage.morphology import binary_erosion, generate_binary_structure

__all__ = ["create_outline", "apply_colour_to_mask", "create_legend"]


def create_outline(mask, width=2, colour=None):
    """Create the outline of the given mask.

    The outline is contained within each structure so that the outer boundary
    of the outline is the outer boundary of the structures.

    Arguments
    ---------
    mask : np.ndarray
        Binary numpy array to find the outline of.
    width : int
        Width of boundary
    colour : Matplotlib colour
        Any input that can be used to specify colour in matplotlib.
        See ``matplotlib.to_rgba`` for usage.
    """
    inner = mask.astype(float)
    structure = generate_binary_structure(inner.ndim, 1).astype(float)
    for _ in range(width):
        inner = binary_erosion(inner, structure=structure)

    outline = mask.astype(float) - inner
    outline *= mask
    if colour is not None:
        return apply_colour_to_mask(outline, colour)
    return outline


def apply_colour_to_mask(mask, colour):
    """Set the mask colour equal to a given colour.

    Takes binary mask as input and sets the colour of pixels
    with value equal to 1 to the specified colour and the rest
    to be transparent.

    Arguments
    ---------
    mask : np.ndarray
        Binary mask to colourise
    colour : Matplotlib colour
        Any input that can be used to specify colour in matplotlib.
        See ``matplotlib.to_rgba`` for usage.

    Returns
    -------
    colourised_mask : np.ndarray
        Image in which all zero-valued pixels in the input mask is transparent and
        all nonzero-valued pixels in the input mask is equal to the specified colour.
    """
    colour = mcolors.to_rgba(colour)
    colour = np.asarray(colour)
    colour = colour[tuple(np.newaxis for _ in range(mask.ndim))]
    mask = mask[..., np.newaxis].astype(bool)

    return mask * colour


def create_legend(colours, labels, ax=None, *args, **kwargs):
    """Create a legend with given colours and labels.

    Additional args and kwargs are passed to matplotlib legend call.

    Arguments
    ---------
    colours : List of Matplotlib colours
        List where each element can be used as a colour in Matplotlib.
    labels : List of strings
        List where the first element is the label of the first colour
        in ``colours``, and so on.
    ax : matplotlib.axes.Axes or None
        Matplotlib axes to place the legend inside. If equal to None,
        then current active axes is used (``ax = plt.gca()``).
    *args
        Passed to ax.legend
    **kwargs
        Passed to ax.legend

    Returns
    -------
    legend : matplotlib.legend.Legend
        The generated legend.
    """
    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color=(0, 0, 0, 0),
            label=label,
            markeredgecolor=(0, 0, 0, 0),
            markerfacecolor=colour,
            markersize=10,
        )
        for colour, label in zip(colours, labels)
    ]
    if ax is None:
        ax = plt.gca()

    return ax.legend(handles=legend_elements, *args, **kwargs)
