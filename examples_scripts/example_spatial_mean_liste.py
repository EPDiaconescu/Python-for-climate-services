import time
import numpy as np
import pandas as pd
import xarray
import glob, os

def spatial_mean_liste(input,liste, var, save_CSV='NO'):
    """ This function will open all netcDF files, make a area-weighted averages of gridded spatial data fo each file 
    and save them into one csv file. 
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	input = put here the path to the netCDF files
	liste = put here the list with the names of all netCDF files you want
	var = put here the name of the variable, ex. 'tas'
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    fld = liste[:1][0]
    ds = xarray.open_dataset(input+fld, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    dataSel = ds[var]
    lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
    wgtmat = np.cos(np.deg2rad(latsM))
    mean_Var = np.zeros(dataSel.time.size)  # Preallocate
    for i in range(dataSel.time.size):
        mean_Var[i] = np.nansum(dataSel.values[i] * wgtmat) / (wgtmat).sum()

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

        dataSel = ds[var]
        lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
        wgtmat = np.cos(np.deg2rad(latsM))
        mean_Var = np.zeros(dataSel.time.size)  # Preallocate
        for i in range(dataSel.time.size):
            mean_Var[i] = np.nansum(dataSel.values[i] * wgtmat) / (wgtmat).sum()
        t = pd.to_datetime(dataSel.time.values)
        timestring = pd.Series(t.strftime('%Y-%m-%d'))
        table[nameModel]=pd.DataFrame(mean_Var, index=timestring, columns=[nameModel])

    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',')
    return table
################### EXAMPLE ##############

start = time.time()

###########################################
# Put in input the path and the netCDF file you want
input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# Put in output the path and the name of the file you want to create
output='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# Put here the name of the CSV file
fileout = 'test1A.csv'

# Put here the name of the netCDF variable
varName='tas'

# first we go in the directory indicated in input
os.chdir(input)

liste=glob.glob('tas_hist_gf*.nc')

dataS= spatial_mean_liste(input, liste, varName, save_CSV=output+fileout)

#####################################

print('It took', time.time()-start, 'seconds.')
