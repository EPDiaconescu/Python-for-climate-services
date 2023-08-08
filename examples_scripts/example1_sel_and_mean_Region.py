import time
import numpy as np
import pandas as pd
import xarray
import glob, os

def sel_and_mean_Region(file,var,lat_bottom, lat_top, lon_left, lon_right, show_regInfo='YES', save_CSV='NO'):
    """ This function will open an netcDF file, select data situated into a rectangle defined by the closest points to lat_bottom, 
	lat_top, lon_left, lon_right, make an area-weighted average of gridded spatial data and save the new file. 
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	file = put here the path and the name of the original netCDF file
	var = put here the name of the variable, ex. 'tas'
	lat_bottom, lat_top, lon_left, lon_right= put here the approximative coordinates of the region
	show_newPer= put 'YES' if you want to verify the lat and lon selected
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
	
    latB = ds.lat.sel(lat=lat_bottom, method='nearest', tolerance=5)
    latT = ds.lat.sel(lat=lat_top, method='nearest', tolerance=5)
    lonL = ds.lon.sel(lon=lon_left, method='nearest', tolerance=5)
    lonR = ds.lon.sel(lon=lon_right, method='nearest', tolerance=5)
    dataSel = ds.sel(lat=slice(latB.values, latT.values), lon=slice(lonL.values, lonR.values))
    lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
    wgtmat = np.cos(np.deg2rad(latsM))
    mean_Var = np.zeros(dataSel.time.size)  # Preallocation

    for i in range(dataSel.time.size):
        mean_Var[i] = np.nansum(dataSel[var].values[i] * wgtmat) / (wgtmat).sum()  

    if show_regInfo=='YES':
        print('There are ' + str(dataSel.lat.values.size) + ' grid points for latitudes')
        print('The first latitude is : ' + str(dataSel.lat.values[0]))
        print('The second latitude is : ' + str(dataSel.lat.values[1]))
        print('The last latitude is : ' + str(dataSel.lat.values[-1]))
        print('  ')
        print('There are ' + str(dataSel.lon.values.size) + ' grid points for longitude')
        print('The first longitude is : ' + str(dataSel.lon.values[0]))
        print('The second longitude is : ' + str(dataSel.lon.values[1]))
        print('The last longitude is : ' + str(dataSel.lon.values[-1]))
        print('  ')
    YYstring1=pd.Series(ds['time.year'].values)
    MMstring1=pd.Series(ds['time.month'].values)
    DDstring1=pd.Series(ds['time.day'].values)
    values=pd.Series(mean_Var)
    table = pd.concat( [YYstring1, MMstring1, DDstring1, values], axis=1)
    table.columns=['year', 'month', 'day', 'Spatial mean']

    
    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',',index=False)
    return table

################ EXAMPLE 1 #######################
#we start a chronometer
start = time.time()

# Put in input the path to the netCDF file you want
input= 'R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# Put here the name of the netCDF file
fld='tasmax_day_BCCAQ2_CanESM2_rcp85_r1i1p1_20960101-21001231.nc'
# Put in output the path to the folder were you want to save the new csv file
output='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'
# Put here the name of the new csv file
new_fld='test_mean.csv'

# Put here the name of the netCDF variable
varName='tasmax'

# Put here the corners of the region you want
# Attention aux longitude if expressed in values from -180 to 180 or from 0 to 360; use the format of your data
lat_bottom=41
lat_top=66.3
lon_left=-88.5
lon_right=-54.5


# we apply the function and we name also the new csv data to dataS to use it further in python
dataS= sel_and_mean_Region(input+fld, varName, lat_bottom, lat_top, lon_left, lon_right, show_regInfo='YES', save_CSV=output+new_fld)

# if we want to have a quick view of the new data:
dataS

# if we want a quick plot of the data
#dataS.index=dataS['date']
#dataS['Spatial mean'].plot()

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')

