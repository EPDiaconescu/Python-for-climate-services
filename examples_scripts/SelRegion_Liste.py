# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 15:48:12 2019

@author: pomeroyc
"""

import xarray
import pandas as pd
import threddsclient
import numpy as np
import os, glob


#List of all the climate indices, RCPs, and percentiles

vars=['cdd']

rcps=['rcp26','rcp45','rcp85']

#lat lon bounds
lat_bottom=40
lat_top=50
lon_left=-70
lon_right=-60

# Date Range
first_date='1950-01-01'
last_date='2100-01-01'

#Specify 'YS' for annual, or 'MS' for monthly
ts = 'YS'

#For specific monthly values, specify in this line below in this format: 'January', leave '' if not relevant 
#Make sure ts is 'MS'
month=''

#Specify where files are located
input='P:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/data_UNECE_cdd/'
#Specify location you want the file saved
output='C:/Users/pomeroyc/Desktop/SupportDesk/'


"""
############################################################################################################################################################################################################
################Don't change anything below here##################################################################################################################################
##############################################################################################################################################################################################
"""

os.chdir(input)
liste=glob.glob('*.nc')

n=len(liste)

for n_ in range(0,n):
    r1=liste[n_]
    varN=r1.split("_")[-2]
    modN=r1.split("_")[-6]
    rcpN=r1.split("_")[-5]
    ds = xarray.open_dataset(r1)
    ds['time'] = xarray.decode_cf(ds).time
    latB = ds.lat.sel(lat=lat_bottom, method='nearest', tolerance=5)
    latT = ds.lat.sel(lat=lat_top, method='nearest', tolerance=5)
    lonL = ds.lon.sel(lon=lon_left, method='nearest', tolerance=5)
    lonR = ds.lon.sel(lon=lon_right, method='nearest', tolerance=5)
    dataSel = ds[varN].sel(lat=slice(latB.values, latT.values), lon=slice(lonL.values, lonR.values),time=slice(first_date,last_date))
    dataSel.to_netcdf(output+'BCCAQv2'+'_'+varN+'_'+modN+'_'+rcpN+'.nc')