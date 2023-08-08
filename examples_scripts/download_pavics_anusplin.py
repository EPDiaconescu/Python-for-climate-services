# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:58:42 2019

@author: DiaconescuE
"""

import threddsclient
import xarray as xr
import numpy as np
import time
import glob, os
import urllib

######################################################################
# This script download from the portal climate indices indicated in 
# the list of climate indices for the RCPs indicaled in the list of RCPs, 
# and for the models indicated in the list of models
#####################################################################

# put here the name of index
indexes = ['tasmax']

# put here the rcp
rcps = ['monthly']

# put here the models
mods = ['nrcan_northamerica']


# folder location to save the original netcdf files
outpath = 'C:/Users/DiaconescuE/Desktop/Anuasplin_monthly/'

if not glob.os.path.exists(outpath):
    glob.os.makedirs(outpath)


# loop through indices and rcps
for ind in indexes:
    print('Start '+ind)
    for rcp in rcps:
        print('Start '+rcp)
        ######################################################################
        start = time.time()
        # start the download of all simulations for one index and one RCP
        url = 'https://pavics.ouranos.ca/thredds/catalog/birdhouse/nrcan/nrcan_northamerica_monthly/tasmax/catalog.html'

        # construct the list of netCDF file to download
        list_fld = []
        ncfiles = [ds for ds in threddsclient.crawl(url, depth=10)]

                    
        #  start the download of files
        for l in ncfiles:
            outfile = glob.os.path.join(outpath, l.name)
            if not os.path.exists(outfile):
                try:
                    urllib.request.urlretrieve(l.access_url(), outfile)
                except:
                    print(outfile, ' not completed')
                    os.remove(outfile)

        print('Download finished for '+rcp)
        