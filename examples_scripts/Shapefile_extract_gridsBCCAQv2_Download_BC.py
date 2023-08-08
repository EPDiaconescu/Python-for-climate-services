"""
This script allows the user to extract the grid cells (and their accompanying data) for any Province in Canada
This can be done for annual data or 30y averages
A specific time period can be selected
The output is in netCDF
For spatial averages, see files marked "spatial mean"
To extract multiple shapes in the same netCDF, see files marked "merge"
For other shapefiles look through the folder or use the master file
"""
#%% Run this section first
import xarray as xr
import threddsclient
import salem
from shapely.geometry import Point
import geopandas as gpd
from geopandas.tools import sjoin
import numpy as np
import pandas as pd
import os, glob

#location of your shapefile
input='C:/Users/pomeroyc/Desktop/test_shapes/Canada/'

#Name of shapefile (in your folder)
shp = 'gpr_000b11a_e.shp'


#%% Change output folder to where you want the data to go

#output folder
output='C:/Users/PomeroyC/Desktop/SupportDesk/FPI/'


#%% This section requires the user to examine the shapefile to determine the exact name of their shape
#   To do this, click on "variable explorer" on the right of this page and then click on the "shdf" variable
#   A text box will appear with a table that includes the names of the different regions

#input your region(s) of interest 
regions=['British Columbia']
#%% Create Mask from Shape function

def create_mask_from_shape(ds, poly):
    ds = ds.drop(ds.data_vars)
    ds = ds.drop('time')
    if len(ds.lon.shape) == 1 & len(ds.lat.shape) == 1:
        # create a 2d grid of lon, lat values
        lon1, lat1 = np.meshgrid(np.asarray(ds.lon.values), np.asarray(ds.lat.values))
    else:
        lon1 = ds.lon.values
        lat1 = ds.lat.values

    # create pandas dataframe from netcdf lat lon points
    df = pd.DataFrame(
        {'id': np.arange(0, lon1.size),
         'lon': lon1.flatten(),
         'lat': lat1.flatten()
         }
    )
    df['Coordinates'] = list(zip(df.lon, df.lat))
    df['Coordinates'] = df['Coordinates'].apply(Point)
    # create geodataframe (spatially refernced)
    gdf_pts = gpd.GeoDataFrame(df, geometry='Coordinates')
    gdf_pts.crs = {'init': 'epsg:4326'}

    # spatial join geodata points with region polygons
    pointInPoly = sjoin(gdf_pts, poly, how='left', op='within')
    # extract polygon ids for points
    mask = pointInPoly['index_right']

    mask_2d = np.array(mask).reshape(lat1.shape[0], lat1.shape[1])
    mask_2d = xr.DataArray(mask_2d, coords=ds.coords, dims=ds.dims)
    return mask_2d




#%% Customize your output

#date range? 'YES' or 'NO'
d_r = 'YES'
first_date = '1950-01-01'
last_date = '2100-01-01'

#30y average? 'YES' or 'NO'
t_ave = 'NO'

#List of climate indices 
vars=['tx_mean', 'rx1day']

rcps=['rcp85']
perc = ['p50']

#%%
"""
#################################################################################################
#####################################Don't edit anything below!!##########################################
##################################################################################################
"""
outpath = 'C:/Users/PomeroyC/Desktop/SupportDesk/FPI/outpath/'
os.chdir(outpath)
strng='*.nc'
list_nc = glob.glob(strng)
#%%
poly = salem.read_shapefile(input+shp)
ds = xr.open_dataset(str(list_nc[0].opendap_url()), decode_times=False)
ds['time'] = xr.decode_cf(ds).time
mask_2d = create_mask_from_shape(ds, poly.loc[poly['PRENAME'] == regions[0]])
mask_2d.to_netcdf(os.path.join(os.path.dirname(output), 'mask_BC.nc'))
mask_2d = xr.open_dataset(os.path.join(os.path.dirname(output), 'mask_BC.nc'))
v = list(mask_2d.data_vars)[0]
mask_2d = mask_2d[v]
#%%
for reg in regions:
    for fld in list_nc:
        r=fld
        varNames_1=[]
        varN=r.split("_")[-2]
        fileN=r.split("/")[-1][0:-3]
        print(fileN)
        for p in perc:
            varName_1=varN+'_'+p
            varNames_1.append(varName_1)
            for g in varNames_1:
                ds = xr.open_dataset(r)
                if d_r == 'YES':
                    ds = ds.sel(time=slice(first_date,last_date))
                else:
                    pass
                data_reg = ds.where(mask_2d == 0, drop=True)               
                data_reg.to_netcdf(output+reg+fileN+".nc")