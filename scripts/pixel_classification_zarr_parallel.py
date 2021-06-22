#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2020 University of Dundee.
#
#   Redistribution and use in source and binary forms, with or without modification, 
#   are permitted provided that the following conditions are met:
# 
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#   Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
#   INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#   HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#   OF THE POSSIBILITY OF SUCH DAMAGE.
# Version: 1.0
#

import numpy
import os
import dask.array as da
from dask.diagnostics import ProgressBar
from dask.distributed import Client, LocalCluster
import matplotlib.pyplot as plt

from omero.gateway import BlitzGateway
from getpass import getpass
from collections import OrderedDict

from ilastik import app
from ilastik.applets.dataSelection.opDataSelection import PreloadedArrayDatasetInfo  # noqa

import time
import vigra


# Connect to the server
def connect(hostname, username, password):
    conn = BlitzGateway(username, password,
                        host=hostname, secure=True)
    conn.connect()
    conn.c.enableKeepAlive(60)
    return conn


# Load-images
def load_images(conn, dataset_id):
    return conn.getObjects('Image', opts={'dataset': dataset_id})


# Load-binary
def load_from_s3(image_id, resolution='0'):
    endpoint_url = 'https://minio-dev.openmicroscopy.org/'
    root = 'idr/outreach/%s.zarr/' % image_id
    # data.shape is (t, c, z, y, x) by convention
    with ProgressBar():
        data = da.from_zarr(endpoint_url + root)
        values = data[:]
        # re-order tczyx -> tzyxc as expected by the ilastik project
        values = values.swapaxes(1, 2).swapaxes(2, 3).swapaxes(3, 4)
        return numpy.asarray(values)


# Analyze-data
def analyze(image_id, model):
    args = app.parse_args([])
    args.headless = True
    args.project = model
    args.readonly = True
    shell = app.main(args)
    input_data = load_from_s3(image_id)
    # run ilastik headless
    data = [ {"Raw Data": PreloadedArrayDatasetInfo(preloaded_array=input_data, axistags=vigra.defaultAxistags("tzyxc"))}]  # noqa
    return shell.workflow.batchProcessingApplet.run_export(data, export_to_array=True)  # noqa


# Prepare-call
def prepare(client, images, model):
    futures = [client.submit(analyze, i.getId(), model) for i in images]
    return futures


# Gather
def gather_results(client, futures):
    return client.gather(futures)


# Disconnect
def disconnect(conn):
    conn.close()


# Save results
def save_results(results):
    for i, r in enumerate(results):
        for d in r:
            # Re-organise array from tzyxc to zctyx order expected by OMERO
            d = d.swapaxes(0, 1).swapaxes(3, 4).swapaxes(2, 3).swapaxes(1, 2)
            value = "image_%s.png" % i
            plt.imsave(value, d[0, 0, 0, :, :])


# main
def main():
    # Collect user credentials
    try:
        host = input("Host [wss://outreach.openmicroscopy.org/omero-ws]: ") or 'wss://outreach.openmicroscopy.org/omero-ws'  # noqa
        username = input("Username [trainer-1]: ") or 'trainer-1'
        password = getpass("Password: ")
        dataset_id = input("Dataset ID [6161]: ") or '6161'
        # Connect to the server
        conn = connect(host, username, password)

        # path to the ilastik project
        ilastik_project = "../notebooks/pipelines/pixel-class-133.ilp"

        # Load the images in the dataset
        images = load_images(conn, dataset_id)

        # prepare ilastik
        os.environ["LAZYFLOW_THREADS"] = "2"
        os.environ["LAZYFLOW_TOTAL_RAM_MB"] = "2000"

        # Create-client
        cluster = LocalCluster()
        client = Client(cluster)
        # End-client

        futures = prepare(client, images, ilastik_project)

        start = time.time()
        results = gather_results(client, futures)
        done = time.time()
        elapsed = (done - start) // 60
        print("Compute time (in minutes): %s" % elapsed)
        save_results(results)
    finally:
        disconnect(conn)

    print("done")


if __name__ == "__main__":
    main()
