Getting Started: Folder Setup
======================================================

To follow this tutorial and run the provided code examples successfully, please follow these steps:

1. **Create a tutorial folder** on your computer called ``marsh_tutorial/``).
2. **Download the model input data here**:
    `model_input_X_L.zip <https://github.com/christineschottmueller/x-marsh/releases/download/v1.0-data/model_input_X_L.zip>`_
   - Extract the archive so that the folder ``model_input_X_L`` is located inside your tutorial folder.
3. **Create an output folder** in your tutorial folder and name it ``model_output_M``.


   Your directory should now look like this:

   .. code-block:: none

       marsh_tutorial/
	   ├── model_input_X_L/
	   │   ├── tidal_projections/
	   │   └── regional_slr_single_rcp/
	   ├── model_output_M.ipynb
	   └── your_notebook.ipynb


  

4. **Run the Jupyter Notebook from within the** ``marsh_tutorial/`` **folder**.

   This ensures that all relative file paths used in the tutorial code (e.g., loading tidal or SLR data) will resolve correctly.

   In the notebook, you can confirm the working directory like this:

   .. code-block:: python

       import os
       print(os.getcwd())

   If needed, change it:

   .. code-block:: python

       os.chdir('path/to/marsh_tutorial/')
