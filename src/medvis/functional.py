"""Tools for overlaying functional imaging data onto structural data.
"""

__author__ = "Yngve Mardal Moe"


import matplotlib.cm as cm
import numpy as np

__all__ = ["apply_cmap_with_blend"]


def apply_cmap_with_blend(functional_data, cmap, vmin=None, vmax=None, gamma=1):
    """Apply a colour map to an array, using the normalised array values as alpha.

    Arguments
    ---------
    functional_data : np.ndarray
        Functional imaging data.
    cmap : str or matplolib colormap
        Which colormap to use.
    vmin : float or None (default=None)
        Minimum value of dynamic range (equivalent to vmin in matplotlib.imshow)
    vmax : float or None (default=None)
        Maximum value of dynamic range (equivalent to vmax in matplotlib.imshow)
    gamma : float (default=1)
        Gamma value used to change the image contrast. No transformation is applied
        if ``gamma=1``

    Returns
    -------
    blended_image : np.ndarray
        RGBA image array with ``functional_data.ndim + 1`` dimensions.
        Last dimension has length 4 and represent the RGBA channels.
    """
    functional_data = functional_data.astype(float)
    if vmin is None:
        vmin = functional_data.min()
    if vmax is None:
        vmax = functional_data.max()
    functional_data = (functional_data - vmin) / (vmax - vmin)
    functional_data = np.minimum(np.maximum(functional_data, 0), 1) ** gamma
    image = cm.get_cmap(cmap)(functional_data)
    image[..., -1] = functional_data

    return image
