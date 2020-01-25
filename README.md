# Guide on how to integrate ilastik and OMERO


This guide demonstrates how to use ilastik to analyze data stored in [IDR](https://idr.openmicroscopy.org/) or an OMERO server.

This repository contains documentation and notebooks.

To run the notebooks, build locally with [repo2docker](https://repo2docker.readthedocs.io/).

To build locally:

 * Create a virtual environment and install repo2docker from PyPI.
 * Clone this repository
 * Run ``repo2docker``

```
pip install jupyter-repo2docker
git clone https://github.com/ome/omero-guide-ilastik.git
cd omero-guide-ilastik
repo2docker .
```

This a Sphinx based documentation. 
If you are unfamiliar with Sphinx, we recommend that you first read 
[Getting Started with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html).
