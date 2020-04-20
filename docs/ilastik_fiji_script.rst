**Use ilastik using Fiji scripting facility**
=============================================

**Description**
---------------

In this section, the segmentation (using Pixel classification routine
of ilastik) of the multi-z images is run in a batch mode.
For this we provide scripts which run ilastik in a headless mode. 
The scripts provide for ilastik a batch of images (coming from an OMERO Dataset) and ilastik is segmenting these
images according to the parameters configured and saved in the ``ilp`` in
the manual step above. We offer two scripts covering this workflow, one
running in Fiji, and the other using the python frames to export images
directly from OMERO to the ilastik running headlessly. Also, we describe
in this part how to use ilastik routine Object classification to
classify objects on images from OMERO manually.

We will show:

-  How to run a script in Fiji, consuming the ``ilp`` file and running the segmentation of the images coming from an OMERO Dataset, saving the ROIs on the original images in OMERO

**Setup**
---------

**ilastik installation**

ilastik has been installed on the local machine. See \ https://www.ilastik.org/\  for details.

**ilastik plugin for Fiji installation instructions**

- Start Fiji. Update it (Help > Update ImageJ)
- in the ``Manage Update Sites`` check the checkbox next to the "ilastik" site.
- After the update was successful, restart your Fiji.
- The new ilastik menu item should be under Plugins menu.

Note: The ilastik menu item might be the last in the Plugins dropdown,
not necessarily alphabetically ordered.

**OMERO plugin for Fiji installation instructions**

See \ https://omero-guides.readthedocs.io/en/latest/fiji/docs/installation.html

**Resources**
-------------

-  IDR data (idr0062) \ https://idr.openmicroscopy.org/webclient/?show=project-801

-  Script using Fiji \ https://raw.githubusercontent.com/ome/training-scripts/master/practical/groovy/analyse_dataset_ilastik.groovy

**Step-by-step**
----------------

Scripting workflow on z-stacks using ilastik headless, Fiji and OMERO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Groovy Script run in Fiji, find the script on \ https://raw.githubusercontent.com/ome/training-scripts/master/practical/groovy/analyse_dataset_ilastik.groovy:

#. Open images (one by one) from an OMERO Dataset (hardcoded in the script) into Fiji and export them as h5 to a local folder specified interactively by the user during the run of the script. It is assumed that the folder specified by the user contains the ilastik Project prepared beforehand (see next step below). The export is facilitated by the ilastik plugin for Fiji.

#. Start headless ilastik, using the "Pixel classification:" module (done by the script from Fiji, using the ilastik plugin for Fiji). The script feeds into the "Pixel classification" ilastik module an ilastik Project (``ilp`` file created previously manually using the workflow above), and also the raw h5 image which the script just exported to the local machine from Fjii.

#. The headless ilastik "Pixel classification" module produces "Probabilities" map - this map is immediately opened into Fiji (again going via the ilastik plugin for Fiji).

#. In Fiji, the Analyze Particles plugin is run on the "Probabilities" map to produce ROIs. Once the ROIs are produced, they are saved to OMERO onto the original raw image which was opened by the script as descripted in
the manual workflow.
