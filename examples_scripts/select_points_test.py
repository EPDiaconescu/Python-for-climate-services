#! /usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset,  num2date, date2num
from scipy.spatial import cKDTree
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import matplotlib  as mpl
from matplotlib.colors import Normalize
norm = Normalize()
import xarray as xr
import geopandas as gpd
from shapely.geometry import Point
import os



def lon_lat_to_cartesian(lon, lat, R = 1):
    """
    calculates lon, lat coordinates of a point on a sphere with
    radius R
    """
    lon_r = np.radians(lon)
    lat_r = np.radians(lat)

    x =  R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)
    return x,y,z


def find_index_of_nearest_xy(y_array, x_array, y_point, x_point):
    distance = (y_array-y_point)**2 + (x_array-x_point)**2
    idy,idx = np.where(distance==distance.min())
    return idy[0],idx[0]


def do_all(y_array, x_array, points):
    store = []
    for i in xrange(points.shape[1]):
        store.append(find_index_of_nearest_xy(y_array,x_array,points[1,i],points[0,i]))
    return store

#################################################

varName='pr'

output='C:/Users/DiaconescuE/Desktop/'
input_sim= 'C:/Users/DiaconescuE/Desktop/'
fd='QC_nrcan_anusplin_daily_pr_1950.nc'


nc_fid = Dataset(input_sim+fd, 'r')
modelVar = nc_fid.variables[varName][:,:,:].squeeze()
lats = nc_fid.variables['lat'][:]
lons = nc_fid.variables['lon'][:]
time_m= nc_fid.variables['time'][:]
units = nc_fid.variables['time'].units
calendar = nc_fid.variables['time'].calendar
dates = num2date(time_m[:],units=units,calendar=calendar)
nc_fid.close() 
new_index_sh=[str(date) for date in dates]


ec_id=('no1', 'no2')
lon_st=(-69.2,-70)
lat_st=(59.46,55)
points_lon=np.array(lon_st, dtype=float)
points_lat = np.array(lat_st, dtype=float)

points_Obs=np.append([points_lon], [points_lat], axis=0)

modelMK=modelVar[0,:,:]*0
if lons.min()>0:
    lon2d, lat2d = np.meshgrid(lons-360, lats)
else:
    lon2d, lat2d = np.meshgrid(lons, lats)
lon2d=lon2d+modelMK
lat2d=lat2d+modelMK  

#convert lat/lon to the Cartesian coordinate reference system (CRS):
xs, ys, zs = lon_lat_to_cartesian(lon2d.flatten(), lat2d.flatten())
xt, yt, zt = lon_lat_to_cartesian(points_lon, points_lat)

#Create cKDTree object to represent source grid.
tree = cKDTree(np.array(list(zip(xs, ys, zs))))
#Nearest neighbour interploation:
#find indices of the nearest neighbors in the flattened array
d, inds = tree.query(np.array(list(zip(xt, yt, zt))), k = 1)
#get interpolated field

lon_sh=np.ones(len(inds))
lat_sh=np.ones(len(inds))
data_sh=np.ones((np.shape(modelVar)[0],len(inds)))
for i in range(0,len(inds)):
    lon_sh[i]=lon2d.flatten()[inds[i]]
    lat_sh[i]=lat2d.flatten()[inds[i]]
    for j in range(0,np.shape(modelVar)[0]):
        data_sh[j,i]=(modelVar[j,:,:].flatten())[inds[i]]

print('find the points')

#################################################################

data_shDF0=pd.DataFrame(data_sh)
data_shDF0.columns=ec_id
data_shDF0.index=new_index_sh

lons_shDF=pd.DataFrame(lon_sh).transpose()
lons_shDF.columns=ec_id
nslo_shDF.index=['lons']

lats_shDF=pd.DataFrame(lat_sh).transpose()
lats_shDF.columns=ec_id
lats_shDF.index=['lats']


data_sh_Final=data_shDF0.append(lons_shDF).append(lats_shDF)

data_sh_Final.to_csv(output+'test_selectedPoints.csv', sep=',')

points_model=np.append(lons_shDF, lats_shDF, axis=0)
points_model_df=pd.DataFrame(points_model)
points_model_df.columns=ec_id
points_model_df.index=['lon','lat']
points_model_df.to_csv(output+'test_selectedCOORD.csv', sep=',')

print ('OK selection')

####

#####THIS PART CAN BE OPIMISE WITH A LOOP OVER ALL POINTS IN points_model_df
#test selection with xarray using lon and lat identified previously

ds = xr.open_dataset(input_sim+fd, decode_times=False)
ds['time'] = xr.decode_cf(ds).time
lat_m1=59.375000
lon_m1=-69.208336
lat_m2=55.041668
lon_m2=-69.958336

dataSel1 = ds[varName].sel(lat=lat_m1, lon=lon_m1, method='nearest')
dataSel2 = ds[varName].sel(lat=lat_m2, lon=lon_m2, method='nearest')
dataSel1.to_netcdf(output+'test_selectedPoint1.nc')
dataSel2.to_netcdf(output+'test_selectedPoint2.nc')

###this is just a verification for one point
test1=dataSel1.to_series()
test2=data_sh_Final['no1']
test1.values-test2.values[:-2]
