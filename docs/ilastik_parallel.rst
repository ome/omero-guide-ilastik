Run ilastik in parallel using dask
==================================


**Description**
---------------

We will show how to use `dask <https://dask.org/>`_ to analyze images in parallel
using the ilastik API. Binary data are stored in a public S3 repository in the Zarr format.


**Setup**
---------

We recommend to use a Conda environment to install ilastik and the OMERO Python bindings. Please read first :doc:`setup`.


**Step-by-Step**
----------------

In this section, we go through the steps required to analyze the data.
The script used in this document is :download:`pixel_classification_zarr_parallel.py <../scripts/pixel_classification_zarr_parallel.py>`.


Connect to the server:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Connect
    :end-before: # Load-images


Load the images:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Load-images
    :end-before: # Load-binary

Define the analysis function:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Analyze-data
    :end-before: # Prepare-call

Helper function load the binary as a numpy array from the Zarr storage format:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Load-binary
    :end-before: # Analyze-data

Start the Dask client and a local cluster:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Create-client
    :end-before: # End-client

Use the ``Dask Future API``.
The work starts immediately as we submit work to the cluster:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Prepare-call
    :end-before: # Gather

We wait until this work is done and gather the results to our local process:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Gather
    :end-before: # Disconnect

When done, close the session:

.. literalinclude:: ../scripts/pixel_classification_zarr_parallel.py
    :start-after: # Disconnect
    :end-before: # main
