# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 09:47:16 2019

@author: leeca
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature 
import xarray

#put here the PATH to the file
input='C:/Users/leeca/Downloads/BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_1950-2100_gddgrow_5_YS.nc'
ds = xarray.open_dataset(input, decode_times=False)
ds['time'] = xarray.decode_cf(ds).time

#put here the latitude
xc = ds['lat'].values
#put here the longitude
yc=ds['lon'].values

##############################################
#Relative to local area

plt.plot()
ax = plt.axes(projection=ccrs.PlateCarree()) 

#put here the extent of the map like, longitude1, longitude2. latitude1, latitude2
#ax.set_extent([-150, -35, 75, 35])         
ax.set_extent([-80, -60, 60, 45]) 

ax.stock_img()


provinces_50m = cfeature.NaturalEarthFeature('cultural',
                                             'admin_1_states_provinces_lines',
                                             '50m',
                                             facecolor='none')



ax.add_feature(cfeature.LAND) #If I comment this => all ok, but I need 

#try to find black colour for lakes
ax.add_feature(cfeature.LAKES, edgecolor='k')
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.BORDERS, )
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(provinces_50m,edgecolor='gray')
ax.coastlines()

ax.scatter(yc,xc,marker='o', c='r',transform=ccrs.Geodetic()) #yc, xc -- lists or numpy arrays

plt.show()
###################################################################################
#Point relative to Canada
plt.plot()
ax = plt.axes(projection=ccrs.PlateCarree()) 

#put here the extent of the map like, longitude1, longitude2. latitude1, latitude2
ax.set_extent([-150, -35, 75, 35])         
#ax.set_extent([-80, -60, 60, 45]) 

ax.stock_img()


provinces_50m = cfeature.NaturalEarthFeature('cultural',
                                             'admin_1_states_provinces_lines',
                                             '50m',
                                             facecolor='none')



ax.add_feature(cfeature.LAND) #If I comment this => all ok, but I need 

#try to find black colour for lakes
ax.add_feature(cfeature.LAKES, edgecolor='k')
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.BORDERS, )
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(provinces_50m,edgecolor='gray')
ax.coastlines()

ax.scatter(yc,xc,marker='o', c='r',transform=ccrs.Geodetic()) #yc, xc -- lists or numpy arrays
plt.show()