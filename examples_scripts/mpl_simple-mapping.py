# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 12:51:09 2014

@author: DiaconescuE
"""

# example map on North America CORDEX
#for North America the values are:
#rotpole.grid_north_pole_latitude = 42.50
#rotpole.grid_north_pole_longitude = 83.00
#rotpole.north_pole_grid_longitude = 180.0
# must consider lon_0 = rotpole.grid_north_pole_longitude - 180


from __future__ import print_function
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def normalize180(lon):
    """Normalize lon to range [180, 180]"""
    lower = -180.; upper = 180.
    if lon > upper or lon == lower:
        lon = lower + abs(lon + upper) % (abs(lower) + abs(upper))
    if lon < lower or lon == upper:
        lon = upper - abs(lon - lower) % (abs(lower) + abs(upper))
    return lower if lon == upper else lon

nc = Dataset('C:/Users/ChowK/Documents/Request/NB-Stephan/NewBrunswick_TotalSummerPrecip_v2_Trend2.nc')
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]

data = nc.variables['prtot'][20,:,:].squeeze()
data = np.ma.masked_values(data,-999.)
maxrain=data.max()
minrain=data.min()

for i in range(1971,2018): #This loop finds the max and min range throughout period to be used for the colour bar
    data = nc.variables['prtot'][i-1950,:,:].squeeze()
    data = np.ma.masked_values(data,-999.)
    if data.max()>maxrain:
        maxrain = data.max()
    if data.min()<minrain:
        minrain = data.min()

for i in range(1970,2018):
    data = nc.variables['prtot'][i-1950,:,:].squeeze()
    data = np.ma.masked_values(data,-999.)

    rotpole_grid_north_pole_latitude = 42.50
    rotpole_grid_north_pole_longitude = 83.00
    rotpole_north_pole_grid_longitude = 180.0

    lon_0 = normalize180(rotpole_grid_north_pole_longitude-180.)
    o_lon_p = rotpole_north_pole_grid_longitude
    o_lat_p = rotpole_grid_north_pole_latitude
    print( 'lon_0,o_lon_p,o_lat_p=',lon_0,o_lon_p,o_lat_p)

    plt.figure(figsize=(9,9), dpi = 300) #change the dpi for image resolution
    plt.subplots_adjust(left=0.02,right=0.98,top=0.90,bottom=0.01,wspace=0.05,hspace=0.05)
    width = 600000; height=400000; #Depending on location of province or territory, 
    lon_0 = -66; lat_0 = 46.5      #the values for these 2 lines will need to be adjusted through trial and error 
                                   #to focus on Region of Interest

    m = Basemap(projection = 'aeqd', width = width, height=height, lon_0=lon_0, lat_0=lat_0, resolution='l')
    x,y=m(*np.meshgrid(lons, lats))           
    m.drawcoastlines()
    m.drawcountries(linewidth=1)
    # draw states boundaries (America only)
    m.drawstates(linewidth=0.3)
    m.drawmeridians(np.arange(-70,-40,1),labels=[0,0,0,1], linewidth=0.2)
    m.drawparallels(np.arange(40,90,1),labels=[1,0,0,0], linewidth=0.2)
    
    clev = np.arange(minrain, maxrain, 0.1)
    cs = m.contourf(x,y,data,clev, cmap="RdYlBu")
    cbar = m.colorbar(cs,location='bottom', format='%0.1f', pad="7%")
    cbar.set_label('Total Summer Precipitation (mm)', fontsize = 12, labelpad = 10)    
    plt.title('Total Summer Precipitation for New Brunswick in ' + str(i), fontsize = 16)
    plt.savefig('C:/Users/ChowK/Documents/Request/NB-Stephan/V2/V2_'+str(i)+'_NB_SummerTotalPrecip.png', bbox_inches = 'tight', dpi=300)
    plt.close()

