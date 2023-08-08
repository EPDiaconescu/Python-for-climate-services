import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt

def spatial_mean(file,var, save_CSV='NO'):
    """ This function will open a netcDF file, make a area-weighted averages of gridded spatial data and save the new file. 
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	file = put here the path and the name of the original netCDF file
	var = put here the name of the variable, ex. 'tas'
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    dataSel = ds[var]
    lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
    wgtmat = np.cos(np.deg2rad(latsM))
    mean_Var = np.zeros(dataSel.time.size)  # Preallocation
    for i in range(dataSel.time.size):
        mean_Var[i] = (dataSel.values[i] * wgtmat).sum() / (wgtmat).sum()

    YYstring1=pd.Series(ds['time.year'].values)
    MMstring1=pd.Series(ds['time.month'].values)
    DDstring1=pd.Series(ds['time.day'].values)
    table = pd.concat( [YYstring1, MMstring1, DDstring1], axis=1)
    table = pd.DataFrame(mean_Var, index=[YYstring1, MMstring1, DDstring1], columns=['Mean'])

    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',')
    return table
################### EXAMPLE ##############

start = time.time()

###########################################
# Put in input the path and the netCDF file you want
input= 'C:/Users/smithnicholas/SD_Research/BCCAQv2_Climate_Indices/Formatted_data/BCCAQv2+ANUSPLIN300_CanESM2_historical+rcp85_r1i1p1_1950-2100_txgt_30_YS_2071-2100.nc'
# Put in output the path and the name of the file you want to create
output='C:/Users/smithnicholas/SD_Research/BCCAQv2_Climate_Indices/Formatted_data/BCCAQv2+ANUSPLIN300_CanESM2_historical+rcp85_r1i1p1_1950-2100_txgt_30_YS_2071-2100_mean.csv'

# Put here the name of the netCDF variable
varName='txgt_30'

dataS= spatial_mean(input, varName ,save_CSV=output)

#####################################

print('It took', time.time()-start, 'seconds.')
