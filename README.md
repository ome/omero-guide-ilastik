# Guide on how to integrate ilastik and OMERO
[![Documentation Status](https://readthedocs.org/projects/omero-guide-ilastik/badge/?version=latest)](https://omero-guides.readthedocs.io/en/latest/ilastik/docs/index.html)
[![Actions Status](https://github.com/ome/omero-guide-ilastik/workflows/repo2docker/badge.svg)](https://github.com/ome/omero-guide-ilastik/actions)

The documentation is deployed at [Use Ilastik](https://omero-guides.readthedocs.io/en/latest/ilastik/docs/index.html).

This guide demonstrates how to use ilastik to analyze data stored in [IDR](https://idr.openmicroscopy.org/) or an OMERO server.

This repository contains documentation and notebooks.

Running locally:

Finally, if you would like to install the necessary requirements locally,
we suggest using Mamba:

* If you do not have any pre-existing conda installation, [install Mamba](https://mamba.readthedocs.io/en/latest/installation.html#installation) and use [mambaforge](https://github.com/conda-forge/miniforge#mambaforge). 
* In case you have a pre-existing conda installation, you can install Mamba by either:
  - Using the recommended way to install Mamba from [mambaforge](https://github.com/conda-forge/miniforge#mambaforge). This will not invalidate your conda installation, but possibly your pre-existing conda envs will be in a different location (e.g. ``/Users/USER_NAME/opt/anaconda3/envs/``) then the new mamba envs (e.g. ``/Users/USER_NAME/mambaforge/envs/``). You can verify this by running ``conda env list``. The addition of ``export CONDA_ENVS_PATH=/Users/user/opt/anaconda3/envs/`` into your ``.bashprofile`` or ``.zprofile`` file will fix this. 
  - Use the [Existing conda install](https://mamba.readthedocs.io/en/latest/installation.html#existing-conda-install) way, i.e. run ``conda install mamba -n base -c conda-forge`` whilst in the base environment. This way can take much longer time than the recommended way described above, and might not lead to a successful installation, especially if run on arm64 (Apple Silicon) OS X.

Create the environment running the commands below as written:

For Windows, OS X x86_64 (NOT arm64 Apple Silicon), Linux:

    $ git clone https://github.com/ome/omero-guide-ilastik
    
    $ cd omero-guide-ilastik

    $ mamba env create -f binder/environment.yml

For OS X arm64 Apple Silicon

    $ git clone https://github.com/ome/omero-guide-ilastik 
    
    $ cd omero-guide-ilastik
    
    $ CONDA_SUBDIR=osx-64 mamba env create -f binder/environment.yml

and activate the newly created environment:

    $ conda activate omero-guide-ilastik


Before creating a new environment, remember to deactivate the current one:

    $ conda deactivate

See also [Conda command reference](https://docs.conda.io/projects/conda/en/latest/commands.html).

The following steps are only required if you want to run the notebooks.

* If you have Anaconda installed:
  * Start Jupyter from the Anaconda-navigator
  * In the conda environment, run ``mamba install ipykernel`` (for OS X Apple Silicon ``CONDA_SUBDIR=osx-64 mamba install ipykernel``)
  * To register the environment, run ``python -m ipykernel install --user --name omero-guide-ilastik``
  * Select the notebook you wish to run and select the ``Kernel>Change kernel>Python [conda env:omero-guide-ilastik]`` or ``Kernel>Change kernel>omero-guide-ilastik``
* If Anaconda is not installed:
  * Add the virtualenv as a jupyter kernel i.e. ``ipython kernel install --name "omero-guide-ilastik" --user``
  * Open jupyter notebook i.e. ``jupyter notebook`` and select the ``omero-guide-ilastik`` kernel or ``[conda env:omero-guide-ilastik]`` according to what is available.

  To stop the notebook server, in the terminal where te server is running, press ``Ctrl C``. The following question will be asked in the terminal ``Shutdown this notebook server (y/[n])?``. Enter the desired choice.
```

This a Sphinx based documentation. 
If you are unfamiliar with Sphinx, we recommend that you first read 
[Getting Started with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html).
