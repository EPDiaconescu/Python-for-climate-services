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
indexes = ['tn_min']

# put here the rcp
rcps = ['rcp85']

# put here the models
mods = ['CanESM2']

#mods = ['BNU-ESM', 'CCSM4', 'CESM1-CAM5', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 'FGOALS-g2', 'GFDL-CM3','GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-AO',
# 'HadGEM2-ES', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM-CHEM', 'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR',
# 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M',
# 'NorESM1-ME', 'bcc-csm1-1-m', 'bcc-csm1-1']

# use YS for annual indices and MS for monthly indices
type='YS'

# folder location to save the original netcdf files
outpath = 'C:/Users/DiaconescuE/Desktop/BCCAQ_v2_Variables/'

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
        url = 'https://pavics.ouranos.ca/thredds/catalog/birdhouse/cccs_portal/indices/Final/BCCAQv2/' + ind + '/'+type+'/' + rcp + '/simulations/catalog.html'

        # construct the list of netCDF file to download
        list_fld = []
        for m in mods:
            ncfiles = [ds for ds in threddsclient.crawl(url, depth=10) if m + '_' in ds.name]
            for n in ncfiles:
                if 'r1i1p1' in n.name:
                    list_fld.append(n)
                    
        #  start the download of files
        for l in list_fld:
            outfile = glob.os.path.join(outpath, l.name)
            urllib.request.urlretrieve(l.access_url(), outfile)

        print('Download finished for '+rcp)
        