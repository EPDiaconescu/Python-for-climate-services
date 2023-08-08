# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature 
import xarray



#put here the latitude
xc =48.9719980
#put here the longitude
yc=-76.9219820

ax = plt.axes(projection=ccrs.PlateCarree()) 

#put here the extent of the map like, longitude1, longitude2. latitude1, latitude2
#ax.set_extent([-80, -70, 40, 50])         
ax.set_extent([-150, -35, 75, 35]) 
ax.stock_img()


provinces_50m = cfeature.NaturalEarthFeature('cultural',
                                             'admin_1_states_provinces_lines',
                                             '50m',
                                             facecolor='none')

ax.add_feature(cfeature.LAND) #If I comment this => all ok, but I need 
ax.add_feature(cfeature.LAKES, edgecolor='k')
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(provinces_50m, edgecolor='gray')
ax.coastlines()

ax.scatter(yc,xc,marker='o', c='r',transform=ccrs.Geodetic()) #yc, xc -- lists or numpy arrays

plt.show()

