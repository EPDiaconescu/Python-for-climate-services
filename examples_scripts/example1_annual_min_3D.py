import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt


#####################################
def annual_min_3D(file, show_newPer='YES', save_nerCDF='NO'):
    """ This function will open an 3D netcDF file, compute the time minimum for each year and save the new 3D file in netCDF.
	The date indicated for each year is the first time step of the corresponding year.
	file = put here the path and the name of the original netCDF file
	show_newPer= put 'YES' if you want to verify the time dimension information
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    new_data=ds.resample(time="AS").min('time')
    new_data.attrs['Description'] = ' annual minimum values '
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


# Put in input the path and the netCDF file you want
input= 'G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/tasAnualMean_CCCma-CanRCM4_NA22_CanESM2_rcp85_yy.nc'
# Put in output the path and the name of the file you want to create
output='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/test_annual_min.nc'

# I will use the following line if I want just to use the resulting line in python for other computations and not save the file 
# (it will be the dataT variable)
dataT=annual_min_3D(input, show_newPer='YES', save_nerCDF='NO')

# I will use the following line if I want to save the new file as netCDF 
annual_min_3D(input, show_newPer='YES', save_nerCDF=output)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
