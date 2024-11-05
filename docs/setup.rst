Install ilastik and OMERO Python bindings
==========================================

In this section, we show how to install ilastik in a virtual environment.
We will use the ilastik API to analyze data stored in an OMERO server. We will use OMERO.py to interact with the OMERO server.

Setup
-----

We recommend to install the dependencies using `Conda <https://docs.conda.io>`_.
In case you do not have a conda installation we recommend downloading and installing the latest version of `Miniforge <https://github.com/conda-forge/miniforge>`_.

Create the environment running the commands below as written:

    $ git clone https://github.com/ome/omero-guide-ilastik
    
    $ cd omero-guide-ilastik

    $ conda env create -f binder/environment.yml

and activate the newly created environment::

    $ conda activate omero-guide-ilastik


Before creating a new environment, remember to deactivate the current one::

    $ conda deactivate

See also `Conda command reference <https://docs.conda.io/projects/conda/en/latest/commands.html>`_.

The following steps are only required if you want to run the notebooks.

* If you installed Miniforge:

  * Open jupyter notebook i.e. ``jupyter notebook`` and select the ``omero-guide-ilastik`` kernel or ``[conda env:omero-guide-ilastik]`` according to what is available.

  To stop the notebook server, in the terminal where te server is running, press ``Ctrl C``. The following question will be asked in the terminal ``Shutdown this notebook server (y/[n])?``. Enter the desired choice.

* If you have an Anaconda installation:

  * Start Jupyter from the Anaconda-navigator
  * To register the environment, run ``python -m ipykernel install --user --name omero-guide-ilastik``
  * Select the notebook you wish to run and select the ``Kernel>Change kernel>Python [conda env:omero-guide-ilastik]`` or ``Kernel>Change kernel>omero-guide-ilastik``.
