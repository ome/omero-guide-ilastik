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

import numpy
import os
import dask.array as da
from dask.diagnostics import ProgressBar
from dask.distributed import Client, LocalCluster

from omero.gateway import BlitzGateway
from getpass import getpass
from collections import OrderedDict

import ilastik_main
from ilastik.applets.dataSelection.opDataSelection import PreloadedArrayDatasetInfo  # noqa

import time


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
    args = ilastik_main.parse_args([])
    args.headless = True
    args.project = model
    args.readonly = True
    shell = ilastik_main.main(args)
    input_data = load_from_s3(image_id)
    # run ilastik headless
    data = OrderedDict([
        (
            "Raw Data",
            [PreloadedArrayDatasetInfo(preloaded_array=input_data)],
        )])
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
        gather_results(client, futures)
        done = time.time()
        elapsed = done - start
        print(elapsed)
    finally:
        disconnect(conn)

    print("done")


if __name__ == "__main__":
    main()
