#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2020 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# FPBioimage was originally published in
# <https://www.nature.com/nphoton/journal/v11/n2/full/nphoton.2016.273.html>.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Version: 1.0
#

import tempfile
import tarfile
import numpy
import os
import zarr

import omero.clients
from omero.gateway import BlitzGateway
from getpass import getpass
from collections import OrderedDict

import ilastik_main
from ilastik.applets.dataSelection.opDataSelection import PreloadedArrayDatasetInfo  # noqa


# Connect to the server
def connect(hostname, username, password):
    conn = BlitzGateway(username, password,
                        host=hostname, secure=True)
    conn.connect()
    return conn


# Load-images
def load_images(conn, dataset_id):
    return conn.getObjects('Image', opts={'dataset': dataset_id})


# Create-dataset
def create_dataset(conn, dataset_id):
    dataset = omero.model.DatasetI()
    v = "ilastik_probabilities_from_dataset_%s" % dataset_id
    dataset.setName(omero.rtypes.rstring(v))
    v = "ilatisk results probabilities from Dataset:%s" % dataset_id
    dataset.setDescription(omero.rtypes.rstring(v))
    return conn.getUpdateService().saveAndReturnObject(dataset)


# Load-data
def load_numpy_array(image, path, extension=".tar", resolution=0):
    # load annotation linked to the image. Download in a tmp dir
    for ann in image.listAnnotations():
        if isinstance(ann, omero.gateway.FileAnnotationWrapper):
            name = ann.getFile().getName()
            ns = ann.getNs()
            if (name.endswith(".zip") or  name.endswith(".tar")) and ns is None:
                file_path = os.path.join(path, name)
                f_path = os.path.join(path, name.strip(extension))
                with open(str(file_path), 'wb') as f:
                    for chunk in ann.getFileInChunks():
                        f.write(chunk)
                # extract the file
                if extension == ".tar":
                    tf = tarfile.open(file_path)
                    tf.extractall(path)
                    tf.close()
                    data = zarr.open(f_path)
                    values = data[resolution][:]
                    #from tczyx to tzyxc
                    values = values.swapaxes(1, 2).swapaxes(2, 3).swapaxes(3, 4)
                    return values
                else:
                    data = zarr.open(file_path)
                    return data[:]
    return None


def load_from_s3(image, resolution='0'):
    cache_size_mb = 2048
    id = image.getId()
    cfg = {
        'anon': True,
        'client_kwargs': {
            'endpoint_url': 'https://minio-dev.openmicroscopy.org/',
        },
        'root': 'idr/outreach/%s.zarr' % id
    }
    s3 = s3fs.S3FileSystem(
        anon=cfg['anon'],
        client_kwargs=cfg['client_kwargs'],
    )
    store = s3fs.S3Map(root=cfg['root'], s3=s3, check=False)
    cached_store = zarr.LRUStoreCache(store, max_size=(cache_size_mb * 2**20))
    # data.shape is (t, c, z, y, x) by convention
    data = da.from_zarr(cached_store)
    values = data[:]
    values = values.swapaxes(1, 2).swapaxes(2, 3).swapaxes(3, 4)
    return numpy.asarray(values)


# Analyze-data
def analyze(conn, images, model, new_dataset, extension=".tar", resolution=0):
    # Prepare ilastik
    # temporary directory where to download files
    path = tempfile.mkdtemp()
    if not os.path.exists(path):
        os.makedirs(path)
    
    os.environ["LAZYFLOW_THREADS"] = "2"
    os.environ["LAZYFLOW_TOTAL_RAM_MB"] = "2000"
    args = ilastik_main.parse_args([])
    args.headless = True
    args.project = model
    shell = ilastik_main.main(args)
    for image in images:
        input_data = load_numpy_array(image, path)
        # run ilastik headless
        print('running ilastik using %s and %s' % (model, image.getName()))
        data = OrderedDict([
            (
                "Raw Data",
                [PreloadedArrayDatasetInfo(preloaded_array=input_data)],
            )])
        predictions = shell.workflow.batchProcessingApplet.run_export(data,
                                                                      export_to_array=True)  # noqa
        for d in predictions:
            save_results(conn, image, d, new_dataset, path)


# Save-results
def save_results(conn, image, data, dataset, path):
    filename, file_extension = os.path.splitext(image.getName())
    # Save the probabilities file as an image
    print("Saving Probabilities as zarr file attached to the original Image")
    name = filename + "_Probabilities_zarr.zip"
    desc = "ilastik probabilities from Image:%s" % image.getId()
    # Re-organise array from tzyxc to zctyx order expected by OMERO
    # data = data.swapaxes(0, 1).swapaxes(3, 4).swapaxes(2, 3).swapaxes(1, 2)
    namespace = "ilastik.zarr.demo"
    file_path = os.path.join(path, name)
    with zarr.ZipStore(file_path, mode='w') as store:
            zarr.array(data, store=store, dtype='int16', compressor=zarr.Blosc(cname='zstd'))
    ann = conn.createFileAnnfromLocalFile(file_path, mimetype="application/zip", ns=namespace, desc=desc)
    image.linkAnnotation(ann)

    # Re-organise array from tzyxc to zctyx order expected by OMERO
    data = data.swapaxes(0, 1).swapaxes(3, 4).swapaxes(2, 3).swapaxes(1, 2)

    def plane_gen():
        """
        Set up a generator of 2D numpy arrays.
        The createImage method below expects planes in the order specified here
        (for z.. for c.. for t..)
        """
        size_z = data.shape[0]-1
        for z in range(data.shape[0]):  # all Z sections data.shape[0]
            print('z: %s/%s' % (z, size_z))
            for c in range(data.shape[1]):  # all channels
                for t in range(data.shape[2]):  # all time-points
                    yield data[z][c][t]

    conn.createImageFromNumpySeq(plane_gen(), name, data.shape[0],
                                 data.shape[1], data.shape[2],
                                 description=desc, dataset=dataset)


# Disconnect
def disconnect(conn):
    conn.close()


# main
def main():
    # Collect user credentials
    host = input("Host [wss://workshop.openmicroscopy.org/omero-ws]: ") or 'wss://workshop.openmicroscopy.org/omero-ws'  # noqa
    username = input("Username [trainer-1]: ") or 'trainer-1'
    password = getpass("Password: ")
    dataset_id = input("Dataset ID [6210]: ") or '6210'
    # Connect to the server
    conn = connect(host, username, password)
    
    # path to the ilastik project
    ilastik_project = "../notebooks/pipelines/pixel-class-133.ilp"

    # Load the images in the dataset
    images = load_images(conn, dataset_id)

    new_dataset = create_dataset(conn, dataset_id)

    analyze(conn, images, ilastik_project, new_dataset)

    disconnect(conn)
    print("done")


if __name__ == "__main__":
    main()
