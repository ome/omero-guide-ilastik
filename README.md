# Guide on how to integrate ilastik and OMERO
[![Documentation Status](https://readthedocs.org/projects/omero-guide-ilastik/badge/?version=latest)](https://omero-guides.readthedocs.io/en/latest/ilastik/docs/index.html)
[![Actions Status](https://github.com/ome/omero-guide-ilastik/workflows/build/badge.svg)](https://github.com/ome/omero-guide-ilastik/actions)

The documentation is deployed at [Use Ilastik](https://omero-guides.readthedocs.io/en/latest/ilastik/docs/index.html).

This guide demonstrates how to use ilastik to analyze data stored in [IDR](https://idr.openmicroscopy.org/) or an OMERO server.

This repository contains documentation and notebooks.

Running locally:

Finally, if you would like to install the necessary requirements locally,
we recommend to install the dependencies using [Conda](https://docs.conda.io>).
In case you do not have a conda installation we recommend downloading and installing the latest version of [Miniforge](https://github.com/conda-forge/miniforge>).

Create the environment running the commands below as written:

    $ git clone https://github.com/ome/omero-guide-ilastik
    
    $ cd omero-guide-ilastik

    $ conda env create -f binder/environment.yml

and activate the newly created environment::

    $ conda activate omero-guide-ilastik

Before creating a new environment, remember to deactivate the current one:

    $ conda deactivate

See also [Conda command reference](https://docs.conda.io/projects/conda/en/latest/commands.html).

The following steps are only required if you want to run the notebooks.

* If you installed Miniforge:

  * Open jupyter notebook i.e. ``jupyter notebook`` and select the ``omero-guide-ilastik`` kernel or ``[conda env:omero-guide-ilastik]`` according to what is available.

  To stop the notebook server, in the terminal where te server is running, press ``Ctrl C``. The following question will be asked in the terminal ``Shutdown this notebook server (y/[n])?``. Enter the desired choice.

* If you have an Anaconda installation:

  * Start Jupyter from the Anaconda-navigator
  * To register the environment, run ``python -m ipykernel install --user --name omero-guide-ilastik``
  * Select the notebook you wish to run and select the ``Kernel>Change kernel>Python [conda env:omero-guide-ilastik]`` or ``Kernel>Change kernel>omero-guide-ilastik``.

This a Sphinx based documentation. 
If you are unfamiliar with Sphinx, we recommend that you first read 
[Getting Started with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html).
