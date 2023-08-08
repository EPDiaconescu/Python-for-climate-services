# -*- coding: utf-8 -*-
"""
Created on Fri May 17 07:23:27 2019

@author: vanderkampd
"""

from netCDF4 import Dataset

import xarray

def compare_ncdf(filename_sub):
    

  #  nc_sub = Dataset(filename_sub)
    nc_sub2 = xarray.open_dataset(filename_sub)
  #  nc_sub_lat = nc_sub.variables["lat"][:]
   # nc_sub_lat = nc_sub.variables["lon"][:]
   # nc_sub_lat = nc_sub.variables["time"][:]
    
    portal = "https://pavics.ouranos.ca/thredds/catalog/birdhouse/pcic/BCCAQv2/catalog.html"

    allfiles = [ds for ds in threddsclient.crawl(portal,depth=1) if nc_sub2.discription in ds.name] # note depth gives the number of subdirectory levels to crawl (10 is probably bigger than actual number)

   # nc = Dataset(allfiles[0].opendap_url())
    nc2 = xarray.open_dataset(allfiles[0].opendap_url())
    #nc_lat = nc.variables["lat"][:]
   # nc_lat = nc.variables["lon"][:]
   # nc_lat = nc.variables["time"][:]
    
    merged = xarray.merge([nc_sub2,nc2])
    
    return merged
    
    

    
    
    return nc


    
    
    
    