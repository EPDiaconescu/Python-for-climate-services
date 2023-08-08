import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt
import glob, os

#####################################
def annual_smallerEQ_count_3D(file, threshold, varName, show_newPer='YES', save_nerCDF='NO'):
    """ This function will open an 3D netcDF file, for each year and for each grid point counts the number of values
    smaller than or equal to the threshold and save the new file in netCDF.
	The date indicated for each year is the last time step of the corresponding year.
	file = put here the path and the name of the original netCDF file
	threshold = value use as threshold
	varName = name of variable
	show_newPer= put 'YES' if you want to verify the time dimention information
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    ds2 = ds[varName]
    ds3 = ds2.where(ds2 <= threshold)
    ds4=ds3 * 0.0 + 1.0
    new_data=ds4.resample(time="AS").sum('time')
    new_data.attrs['Description'] = ' annual number of values smaller than or equal to '+ str(threshold)
    if show_newPer=='YES':
        print('There are ' + str(new_data.time.values.size) + ' time steps')
        print('The first time stemp is : ' + str(new_data.time.values[0]))
        print('The second time stemp is : ' + str(new_data.time.values[1]))
        print('The last time stemp is : ' + str(new_data.time.values[-1]))

    if save_nerCDF!='NO':
        new_data.to_netcdf(save_nerCDF)
    return new_data

################### EXAMPLE ##############
#we start a cronometer
start = time.time()

# the following script will transform all the files that are in the directory indicated in input and save them in output
input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/WindsorData/dataReq1_rcp85/'
output= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'
threshold=-20.0
varName='tasmin'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas and are ended with _mm.nc
list=glob.glob('tasmin_day*.nc')

# we construct a loop, which will call the function for each files we put in the list

for fld in list[:]:
    print(fld)
    fileout = fld[:-6] + '_annual_number_smallerEQ.nc'
    annual_smallerEQ_count_3D(input+fld, threshold, varName,show_newPer='NO', save_nerCDF=output+fileout)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
