# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:32:17 2019

@author: leeca
"""
#import time
#import pandas as pd
#import xarray
#import glob, os
#import matplotlib as mpl
from netCDF4 import Dataset, num2date
#import numpy as np
from matplotlib import pyplot as plt
#from mpl_toolkits.basemap import Basemap
import threddsclient

from random import sample 

import time


from numpy import float32

#This is with txgt_30, which was used in the email example. Both this variable and the heat wave indices variables did not work
portal = "https://pavics.ouranos.ca/thredds/catalog/birdhouse/pcic/BCCAQv2/catalog.html"
output='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/09 - Portal/daily_download_QA/'

allfiles = [ds for ds in threddsclient.crawl(portal,depth=1)]  # note depth gives the number of subdirectory levels to crawl (10 is probably bigger than actual number)

# Select only files with ‘ensemble-percentiles’ in the filename
selected = sample(allfiles,1)



for fld in selected:
               
            nc = Dataset(fld.opendap_url())
            
            filename = fld.opendap_url().split("/")[-1]
            
            var_name = filename.split("_")[0]
            
            time_sample = sample(range(nc.dimensions['time'].size),1)[0]
              
            data_org = nc.variables[var_name][time_sample,:,:].squeeze()
            lat_org = nc.variables['lat'][:].squeeze()
            lon_org = nc.variables['lon'][:].squeeze()
            time_org = nc.variables['time'][time_sample]
                 
            filename_out = filename.split(".")[0] + "_sub.nc"
            
            my_file = Dataset(filename_out,'w', format = 'NETCDF4')

            my_file.discription = filename
            my_file.history = 'Created on: ' +time.ctime(time.time())
            
            lon = my_file.createDimension('lon',lon_org.size)
            lat = my_file.createDimension('lat',lat_org.size)
            time = my_file.createDimension('time',time_org.size)
            
            #Variables
            latitude = my_file.createVariable('lat',float32,('lat',))
            latitude.units = 'Degree_north'
            longitude = my_file.createVariable('lon',float32,('lon',))
            longitude.units = 'Degree_east'
            time_out = my_file.createVariable('time',float32,('time',))
            time_out.units = nc.variables['time'].units
            time_out.calendar = nc.variables['time'].calendar
            
            data_out = my_file.createVariable(var_name,float32,('lon','lat','time'),fill_value = -9999.0)
            data_out.units = nc[var_name].units
            
                        
            #Load values to the variables
            latitude[:] = lat_org[:]
            longitude[:] = lon_org[:]
            time_out[:] = time_org
            data_out[:,:] = data_org[:,:]
            my_file.close()
                        
          # data0 =nc1.variables[varName][timeI,:,:].squeeze()
          