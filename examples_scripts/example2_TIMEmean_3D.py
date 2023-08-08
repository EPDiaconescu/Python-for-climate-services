import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt
import glob, os

#####################################
def time_mean_3D(file, save_netCDF='NO'):
    """ This function will open an 3D netcDF file, compute the time mean over the entire period and save the new file in netCDF.
	file = put here the path and the name of the original netCDF file
	show_newPer= put 'YES' if you want to verify the time dimension information
	save_netCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    new_data=ds.mean('time', keep_attrs=True)
    new_data.attrs['Description'] = ' time mean '

    if save_netCDF!='NO':
        new_data.to_netcdf(save_netCDF)
    return new_data

################### EXAMPLE ##############
#we start a chronometer
start = time.time()

# the following script will transform all the files that are in the directory indicated in input and save them in output
input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/05 - Personal/Smith/Statistical Downscaling of Climate Models Research/BCCAQv2_Climate_Indices/Formatted_data/'
output='C:/Users/DiaconescuE/Desktop/BCCAQv2_Climate_Indices/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas and are ended with _mm.nc
list=glob.glob('BCCAQ*.nc')
#list=glob.glob('tas*lat45.5_lon284.3.nc')

# we construct a loop, which will call the function for each files we put in the list

for fld in list[:]:
    print(fld)
    fileout = fld[:-6] + '_time_mean.nc'
    time_mean_3D(input+fld, save_netCDF=output+fileout)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
