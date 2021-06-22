/*
 * -----------------------------------------------------------------------------
 *  Copyright (C) 2020 University of Dundee. All rights reserved.
 *
 *
 *  Redistribution and use in source and binary forms, with or without modification, 
 *  are permitted provided that the following conditions are met:
 * 
 *  Redistributions of source code must retain the above copyright notice,
 *  this list of conditions and the following disclaimer.
 *  Redistributions in binary form must reproduce the above copyright notice, 
 *  this list of conditions and the following disclaimer in the documentation
 *  and/or other materials provided with the distribution.
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 *  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
 *  INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 *  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 *  OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ------------------------------------------------------------------------------
 */

/*
 * This Groovy script shows how to analyse an OMERO dataset
 * i.e. a collection of OMERO images using ilastik.
 * Use this script in the Scripting Dialog of Fiji (File > New > Script).
 * Select Groovy as language in the Scripting Dialog.
 * Error handling is omitted to ease the reading of the script but this
 * should be added if used in production to make sure the services are closed
 * Information can be found at
 * https://docs.openmicroscopy.org/latest/omero5/developers/Java.html
 */

#@ String(label="Username") USERNAME
#@ String(label="Password", style='password') PASSWORD
#@ String(label="Host", value='workshop.openmicroscopy.org') HOST
#@ Integer(label="Port", value=4064) PORT
#@ Integer(label="Dataset ID") dataset_id

import java.util.ArrayList


// OMERO Dependencies
import omero.gateway.Gateway
import omero.gateway.LoginCredentials
import omero.gateway.SecurityContext
import omero.gateway.facility.BrowseFacility
import omero.gateway.facility.ROIFacility
import omero.log.SimpleLogger

import org.openmicroscopy.shoola.util.roi.io.ROIReader

import loci.formats.FormatTools
import loci.formats.ImageTools
import loci.common.DataTools

import ij.IJ
import ij.ImagePlus
import ij.ImageStack
import ij.process.ByteProcessor
import ij.process.ShortProcessor
import ij.plugin.frame.RoiManager
import ij.measure.ResultsTable


// Connect to omero
def connect_to_omero() {
    "Connect to OMERO"

    credentials = new LoginCredentials()
    credentials.getServer().setHostname(HOST)
    credentials.getServer().setPort(PORT)
    credentials.getUser().setUsername(USERNAME.trim())
    credentials.getUser().setPassword(PASSWORD.trim())
    simpleLogger = new SimpleLogger()
    gateway = new Gateway(simpleLogger)
    gateway.connect(credentials)
    return gateway

}

// Load-images
def get_images(gateway, ctx, dataset_id) {
    "List all images contained in a Dataset"

    browse = gateway.getFacility(BrowseFacility)
    ids = new ArrayList(1)
    ids.add(new Long(dataset_id))
    return browse.getImagesForDatasets(ctx, ids)
}

// Open-image
def open_image_plus(HOST, USERNAME, PASSWORD, PORT, group_id, image_id) {
    "Open the image using the Bio-Formats Importer"

    StringBuilder options = new StringBuilder()
    options.append("location=[OMERO] open=[omero:server=")
    options.append(HOST)
    options.append("\nuser=")
    options.append(USERNAME.trim())
    options.append("\nport=")
    options.append(PORT)
    options.append("\npass=")
    options.append(PASSWORD.trim())
    options.append("\ngroupID=")
    options.append(group_id)
    options.append("\niid=")
    options.append(image_id)
    options.append("] ")
    options.append("windowless=true view=Hyperstack ")
    IJ.runPlugIn("loci.plugins.LociImporter", options.toString())
}


// Check-exists
def file_exists(name, list) {
    for (i = 0; i < list.length; i++) {
        if (name.equals(list[i].toString())) {
            return true
        }
     }
    return false
}

// Save-rois
def save_rois_to_omero(ctx, image_id, imp) {
    " Save ROI's back to OMERO"
    reader = new ROIReader()
    roi_list = reader.readImageJROIFromSources(image_id, imp)
    roi_facility = gateway.getFacility(ROIFacility)
    result = roi_facility.saveROIs(ctx, image_id, exp_id, roi_list)
}

// Beginning of script
// Choose a directory where to save the .h5 file
data_dir = IJ.getDirectory("Choose a directory where to save h5 files")
if (data_dir == null) {
    println "cancel"
    return
}

pixelClassificationProject = IJ.getFilePath("Choose a ilastik Project File")
if (pixelClassificationProject == null) {
	println "cancel"
	return
}


//Set the path to the executable
IJ.run("Configure ilastik executable location")


// Prototype analysis example
gateway = connect_to_omero()
exp = gateway.getLoggedInUser()
group_id = exp.getGroupId()
ctx = new SecurityContext(group_id)
exp_id = exp.getId()

// get all images in an omero dataset
images = get_images(gateway, ctx, dataset_id)

inputDataset = "[/data]"
dir = new File(data_dir.toString())
files = dir.listFiles()


outputType = "Probabilities" //Default
axisOrder = "tzyxc" //axis of the model
inputDataset = "[/data]"

images.each() { image ->
    id = image.getId()
    name = image.getName() + ".h5"
    output_file = data_dir + name
    // Open the image if the .h5 file does not exist in the directory
    if (!file_exists(output_file, files)) {
        println "opening image from OMERO"
        open_image_plus(HOST, USERNAME, PASSWORD, PORT, group_id, String.valueOf(id))
        //compressionLevel to be added if required
        args = "select=" + output_file
        // Export as h5
        IJ.run("Export HDF5", args);
        imp = IJ.getImage()
        imp.close()
        // Close export
    }
    // Import h5 
    args = "select=" + output_file + " datasetname=" + inputDataset +  " axisorder=" + axisOrder            
    println "opening h5 file"
    IJ.run("Import HDF5", args)
    // run pixel classification
    input_image = output_file + "/data";
    args = "projectfilename=" + pixelClassificationProject + " saveonly=false inputimage=" + input_image + " chosenoutputtype=" + outputType;
    println "running Pixel Classification Prediction"
    IJ.run("Run Pixel Classification Prediction", args);
    // end pixel classification

    //Get the outputType.h5 file e.g. Probabilities.h5
    imp = IJ.getImage()
    // Analyse the images. This section could be replaced by any other macro
    IJ.run("8-bit")
    //white might be required depending on the version of Fiji
    IJ.run(imp, "Auto Threshold", "method=MaxEntropy stack")
    IJ.run(imp, "Analyze Particles...", "size=50-Infinity pixel display clear add stack summarize")
    
    // Save the ROIs back to OMERO
    roivec = save_rois_to_omero(ctx, id, imp)

    // Close windows
    IJ.run("Close")
    // Close the various components
    IJ.selectWindow("Results")
    IJ.run("Close")
    IJ.selectWindow("ROI Manager")
    IJ.run("Close")
    imp.changes = false     // Prevent "Save Changes?" dialog
    imp.close()
    IJ.run("Close All")
}
// Close the connection
gateway.disconnect()
// End
println "processing done"
