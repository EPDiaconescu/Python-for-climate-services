# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 12:01:43 2019

@author: DiaconescuE
"""

import matplotlib.pyplot as plt

import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import cartopy.io.img_tiles as cimgt

extent = [-76.375, -75.125,44.958, 45.875]
xc =45.421532
#put here the longitude
yc=-75.697189



request = cimgt.OSM()

fig = plt.figure(figsize=(9, 13))
ax = plt.axes(projection=request.crs)
gl = ax.gridlines(draw_labels=True, alpha=0.2)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.scatter(yc,xc,marker='o', c='r',transform=ccrs.Geodetic()) #yc, xc -- lists or numpy arrays


ax.set_extent(extent)

ax.add_image(request, 10)
#plt.savefig('Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/05 - Personal/Diaconescu/NCCregion2.png')
plt.show()

