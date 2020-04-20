Track mitosis using ilastik
===========================


**Description**
---------------

In this section, a manual tracking workflow is shown on images of
cells undergoing mitosis. The lineage of the cells is being followed.
The images are timelapses from the Image Data Resource, the “mitocheck”
set. As a result of this step, again, an ``ilp`` file is produced and saved
for further use by the follow-up scripting workflow, similarly to the
steps one and two described for the multi-z images above.


**Setup**
---------

**ilastik installation**

- ilastik has been installed on the local machine. See \ https://www.ilastik.org/\  for details.


**Step-by-step**
----------------

#. Open ilastik, create a new Pixel classification project, feeding in the raw data in h5 form. The data come from \ https://www.ilastik.org/download.html\ , more concretely the "Mitocheck 2D+t" download \ http://data.ilastik.org/mitocheck.zip\ . Download, unzip and feed the h5 file which has not the "export" in its name into this step (Pixel classification).

#. Follow the steps of Pixel classification as described above in the idr0062 workflow - you will have to

   - Adjust the parameters, saving the new project as "mitocheck-pixel-class.ilp"

   - Export "Probabilities", which can be exported as "mitocheck_94570_2D+t_01-53_Probabilities.h5"

   - Close and reopen ilastik. Open the projec "conservationTracking.ilp" from the folder you downloaded from the ilastik site. In the "Raw data", tab of "Input data" make sure the raw data are pointing to where you have your "mitocheck_94570_2D+t_01-53.h5" file locally. Further, in the "Prediction maps" tab of "Input data", exchange the file there by right-clicking on it and selecting the "Replace with file" and replace this file with the "mitocheck_94570_2D+t_01-53_Probabilities.h5" which you exported from the Pixel classification workflow (see points above)

   - Run through the tabs in the LHP, making sure that when Thresholding, you swap the blue and yellow objects (my Pixel class. produced a probabilities map which is swapped in the sense objects vs bckgr coloring). Also, you have to manually select the cells which are dividing and not dividing in the corresponding tabs in LHP in quite a few timeframes, see \ https://www.ilastik.org/documentation/tracking/tracking#3-division-and-object-count-classifiers\  for how to do it.

   - Further, you have to discern false detections, and 1 object and 2 object blobs manually on quite a few frames, the LHP harmonice is called Object Count classification, as described in \ https://www.ilastik.org/documentation/tracking/tracking#3-division-and-object-count-classifiers\ , second part.

   - Once done, in the Tracking tab in left-hand paneHP, click on "Track !" button, making sure you did not change any params inadvertently. This will take a while.

   - Select the “Tracking Results Export” tab in LHP and define your export target dir, then export in a row
         - "mitocheck_94570_2D+t_01-53_Object-Identities.h5",
         - "mitocheck_94570_2D+t_01-53_Tracking-Result.h5",
         - "mitocheck_94570_2D+t_01-53_Merger-Result.h5" and
         - "mitocheck_94570_2D+t_01-53_CSV-Table.h5.csv"

    These are 3 timelapses and one CSV with the tracking results.

   - Save the Project as "mitocheck-tracking-serious.ilp". This is the main starting point for the automatic pipeline from OMERO. The pipeline is

      - "mitocheck-pixel-class.ilp" which

         - consumes the "mitocheck_94570_2D+t_01-53.h5"
         - produces the "mitocheck_94570_2D+t_01-53_Probabilities.h5"

 
      - "Mitocheck-tracking-serious.ilp" which

         - consumes 
            
            - "mitocheck_94570_2D+t_01-53.h5"
            - "mitocheck_94570_2D+t_01-53_Probabilities.h5"

         
         - produces the outputs
            
            - "mitocheck_94570_2D+t_01-53_Object-Identities.h5"
            - "mitocheck_94570_2D+t_01-53_Tracking-Result.h5"
            - "mitocheck_94570_2D+t_01-53_Merger-Result.h5"
            - "mitocheck_94570_2D+t_01-53_CSV-Table.h5.csv"
