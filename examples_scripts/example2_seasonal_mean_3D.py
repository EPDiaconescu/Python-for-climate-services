import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt
import glob, os

#####################################
def seasonal_mean_3D(file, show_newPer='YES', save_nerCDF='NO'):
    """ This function will open an 3D netcDF file, compute the time mean for each season and save the new file in netCDF.
	The date indicated for each season is the last time step of the corresponding season.
	file = put here the path and the name of the original netCDF file
	show_newPer= put 'YES' if you want to verify the time dimension information
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    selperiod_years(input,first_yy, last_yy, show_newPer='YES', save_nerCDF=output)
    new_data=ds.resample(time=selperiod_years).mean('time')
    new_data.attrs['Description'] = ' seasonal mean values '
    if show_newPer=='YES':
        print('There are ' + str(new_data.time.values.size) + ' time steps')
        print('The first time stemp is : ' + str(new_data.time.values[0]))
        print('The second time stemp is : ' + str(new_data.time.values[1]))
        print('The last time stemp is : ' + str(new_data.time.values[-1]))

    if save_nerCDF!='NO':
        new_data.to_netcdf(save_nerCDF)
    return new_data

################### EXAMPLE ##############
#we start a chronometer
start = time.time()

# the following script will transform all the files that are in the directory indicated in input and save them in output
input= 'C:/Users/smithnicholas/SD_Research/BCCAQv2_Climate_Indices/Formatted_data/'
output= 'C:/Users/smithnicholas/SD_Research/BCCAQv2_Climate_Indices/Formatted_data/'

# put here the first and the last year
first_yy='1981'
last_yy='2010'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas and are ended with _mm.nc
list=glob.glob('BCCAQv2*.nc')
#list=glob.glob('tas*lat45.5_lon284.3.nc')

# we construct a loop, which will call the function for each files we put in the list

for fld in list[:]:
    print(fld)
    fileout = fld[:-6] + '_seasonal_mean.nc'
    seasonal_mean_3D(input+fld, show_newPer='NO', save_nerCDF=output+fileout)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
