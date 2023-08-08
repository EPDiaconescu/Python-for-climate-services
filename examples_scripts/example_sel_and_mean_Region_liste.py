import time
import numpy as np
import pandas as pd
import xarray
import glob, os

def sel_and_mean_Region_liste(input,liste,varName,lat_bottom, lat_top, lon_left, lon_right, show_regInfo='YES', save_CSV='NO'):
    """ This function will open several netcDF files, for each of them will select data situated into a rectangle
    defined by the closest points to lat_bottom, lat_top, lon_left, lon_right,
    make an area-weighted average of gridded spatial data and save the information from all models into one CSV file
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	input = put here the path to the netCDF files
	liste = put here the list with the names of all netCDF files you want
	varName = put here the name of the variable, ex. 'tas'
	lat_bottom, lat_top, lon_left, lon_right= put here the approximative coordinates of the region
	show_newPer= put 'YES' if you want to verify the lat and lon selected
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    fld = liste[:1][0]
    ds = xarray.open_dataset(input+fld, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    latB = ds.lat.sel(lat=lat_bottom, method='nearest', tolerance=5)
    latT = ds.lat.sel(lat=lat_top, method='nearest', tolerance=5)
    lonL = ds.lon.sel(lon=lon_left, method='nearest', tolerance=5)
    lonR = ds.lon.sel(lon=lon_right, method='nearest', tolerance=5)
    dataSel = ds.sel(lat=slice(latB.values, latT.values), lon=slice(lonL.values, lonR.values))
    lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
    wgtmat = np.cos(np.deg2rad(latsM))
    mean_Var = np.zeros(dataSel.time.size)  # Preallocate
    for i in range(dataSel.time.size):
        mean_Var[i] = np.nansum(dataSel[varName].values[i] * wgtmat) / (wgtmat).sum()

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
    t = pd.to_datetime(dataSel.time.values)
    timestring = pd.Series(t.strftime('%Y-%m-%d'))
    YYstring = pd.Series(t.strftime('%Y'))
    MMstring = pd.Series(t.strftime('%m'))
    DDstring = pd.Series(t.strftime('%d'))
    values=pd.Series(mean_Var)
    table = pd.concat( [YYstring, MMstring, DDstring, values], axis=1)
    table.columns=['year', 'month', 'day', 'm1']
    table.index = timestring
    print(fld, 'm1')
    for fld, nr in zip(liste[1:], range(2, len(liste) + 2)):
        print(fld, 'm' + str(nr))
        nameModel = 'm' + str(nr)
        ds = xarray.open_dataset(input+fld, decode_times=False)
		ds['time'] = xarray.decode_cf(ds).time
        latB = ds.lat.sel(lat=lat_bottom, method='nearest', tolerance=5)
        latT = ds.lat.sel(lat=lat_top, method='nearest', tolerance=5)
        lonL = ds.lon.sel(lon=lon_left, method='nearest', tolerance=5)
        lonR = ds.lon.sel(lon=lon_right, method='nearest', tolerance=5)
        dataSel = ds.sel(lat=slice(latB.values, latT.values), lon=slice(lonL.values, lonR.values))
        lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
        wgtmat = np.cos(np.deg2rad(latsM))
        mean_Var = np.zeros(dataSel.time.size)  # Preallocate
        for i in range(dataSel.time.size):
            mean_Var[i] = np.nansum(dataSel[varName].values[i] * wgtmat) / (wgtmat).sum()
        t = pd.to_datetime(dataSel.time.values)
        timestring = pd.Series(t.strftime('%Y-%m-%d'))
        table[nameModel]=pd.DataFrame(mean_Var, index=timestring, columns=[nameModel])
    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',')
    return table

############# EXAMPLE 1 ################################
# In this example, we will select all historical files, compute the mean over the desired region
# but save all models into a single csv file, each model on a different column

#we start a chronometer
start = time.time()

# Put in input the path to the netCDF files you want
input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/Temperature/'
# Put in output the path to the folder were you want to save the new csv file
output='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# Put here the corners of the region you want
# Attention aux longitude if expressed in values from -180 to 180 or 0 to 360; use the format of your data
lat_bottom=42.2
lat_top=65.3
lon_left=200.1
lon_right=255.4

# Put here the name of the txt file
new_fld = 'CMIP5_histo_regionalMean_lat'+str(lat_bottom)+'to'+str(lat_top)+'_lon'+str(lon_left)+'to'+str(lon_right)+'.csv'

# Put here the name of the netCDF variable
varName='tas'

# first we go in the directory indicated in input
os.chdir(input)

# we want all historical files
# we construct a list containing all the file in this directory that begin with tas_hist and are ended with .nc
liste=glob.glob('tas_hist*.nc')

# we apply he function
dataS=sel_and_mean_Region_liste(input,liste, varName, lat_bottom, lat_top, lon_left, lon_right, show_regInfo='YES',
                        save_CSV=output+new_fld)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
#file:///W:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/examples_scripts/example2_annual_anomalies_3D_BCCAQ2.py
#file:///W:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/examples_scripts/example_annual_anomalies_1D_BCCAQ2_liste.py
