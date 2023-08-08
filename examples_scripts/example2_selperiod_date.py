import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt


#####################################
def selperiod_date(file,first_date, last_date, show_newPer='YES', save_nerCDF='NO'):
    """ This function will open an netcDF file, select all time steps from the date corresponding to 
	first_date to the date corresponding to the last_date and save the new file in netCDF
	file = put here the path and the name of the original netCDF file
	first_date = date from which the selection begins ; ex. '2000-02-15'
	last_date = last date in the selected period; ex. '2002-10-10'
	show_newPer= put 'YES' if you want to verify the years selected
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    new_data=ds.sel(time=slice(first_date,last_date))
    if show_newPer=='YES':
        print('There are ' + str(new_data.time.values.size) + ' time steps')
        print('The first time stemp is : ' + str(new_data.time.values[0]))
        print('The second time stemp is : ' + str(new_data.time.values[1]))
        print('The last time stemp is : ' + str(new_data.time.values[-1]))

    if save_nerCDF!='NO':
        new_data.to_netcdf(save_nerCDF)
    return new_data

################### EXAMPLE ##############

start = time.time()

###########################################
# Put in input the path to the folder containing the files
input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# Put in output the path to the folder where you want to save the new files
output='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# put here the first and the last date
first_date='2000-02-14'
last_date='2002-10-10'

# first we go in the directory indicated in input
os.chdir(input)

# we want all historical files
# we construct a list containing all the file in this directory that begin with tas_hist and are ended with .nc
list=glob.glob('tas_hist*.nc')

# we construct a loop, which will call the function for each files we put in the list
for fld in list[:]:
    print(fld)
    new_file = fld[:-3] + '_new.nc'
    selperiod_date(input+fld, first_date,last_date, show_newPer='NO', save_nerCDF=output+new_file)

print('It took', time.time()-start, 'seconds.')
