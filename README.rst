======
MedVis
======

Tools to visualise medical images.

To install, run

.. code::

    pip install medvis

The following example will plot a PET/CT image with alpha blended PET signal ontop
of a grayscale CT image. The outline of two masks are shown with a legend that specifies
what the different colours represent.

.. code:: python

        import matplotlib.pyplot as plt
        import medvis
        
        
        ct_image = ...
        pet_image = ...
        binary_true_mask = ...
        binary_pred_mask = ...

        true_colour = "tomato"
        pred_colour = "skyblue"

        blended_pet_image = medvis.apply_cmap_with_blend(pet_image, 'magma')
        true_mask_outline = medvis.create_outline(binary_true_mask, width=2, colour=true_colour)
        pred_mask_outline = medvis.create_outline(binary_pred_mask, width=2, colour=pred_colour)

        fig, ax = plt.subplots()
        ax.imshow(ct_image, cmap='gray')
        ax.imshow(blended_pet_image)
        ax.imshow(true_mask_outline)
        ax.imshow(pred_mask_outline)
        medvis.create_legend([true_colour, pred_colour], ["True mask", "Predicted mask"], ax=ax)

        plt.show()
        
