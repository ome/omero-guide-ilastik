Getting started with ilastik API and OMERO
==========================================

**Description**
---------------

We will use a Python script showing how to analyze data stored in an OMERO server
using the ilastik API. The code snippets are extracted from the Python script
:download:`pixels_classification.py <../scripts/pixels_classification.py>`. A notebook
is also available, see `pixels_classification.ipynb <https://mybinder.org/v2/gh/ome/omero-guide-ilastik/master?filepath=notebooks>`_.


We will show:

- How to connect to server

- How load images from a dataset using the OMERO API.

- How to run ilastik using its Python API.

- How to save the generated results as OMERO images.

**Resources**
-------------

We will use an ilastik project created with ilastik version 1.3.3 to analyse 3D tissues
data from the Image Data Resource (IDR).

- :download:`ilastik model <../notebooks/pipelines/pixel-class-133.ilp>`
- IDR data \ https://idr.openmicroscopy.org/webclient/?show=project-801

For convenience, the IDR data have been imported into the training
OMERO.server. This is only because we cannot save results back to IDR
which is a read-only OMERO.server.

**Setup**
---------

We recommend to use a Conda environment to install ilastik and the OMERO Python bindings. Please read first :doc:`setup`.

**Step-by-Step**
----------------

In this section, we go over the various steps required to analyse the data.
The script used in this document is :download:`pixels_classification.py <../scripts/pixels_classification.py>`.

Connect to the server:

.. literalinclude:: ../scripts/pixels_classification.py
    :start-after: # Connect
    :end-before: # Load-images


Load the images:

.. literalinclude:: ../scripts/pixels_classification.py
    :start-after: # Load-images
    :end-before: # Create-dataset


We are now ready to analyze the images:

.. literalinclude:: ../scripts/pixels_classification.py
    :start-after: # Analyze-data
    :end-before: # Save-results


The ilastik project used expects the data array to be in the order **TZYXC**.
The order will need to be adjusted depending on the order expected in the ilastik project

.. literalinclude:: ../scripts/pixels_classification.py
    :start-after: # Load-data
    :end-before: # Analyze-data

Let's now save the generated data and create a new OMERO image:

.. literalinclude:: ../scripts/pixels_classification.py
    :start-after: # Save-results
    :end-before: # Disconnect


When done, close the session:

.. literalinclude:: ../scripts/pixels_classification.py
    :start-after: # Disconnect
    :end-before: # main


**Exercises**
-------------

