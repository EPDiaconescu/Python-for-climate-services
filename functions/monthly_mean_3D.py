import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt


#####################################
def monthly_mean_3D(file, show_newPer='YES', save_nerCDF='NO'):
    """ This function will open an 3D netcDF file, compute the time mean for each month and save the new file in netCDF.
	The date indicated for each year is the first time step of the corresponding month.
	file = put here the path and the name of the original netCDF file
	show_newPer= put 'YES' if you want to verify the time dimension information
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file)
    new_data=ds.resample(time='M').min('time')
    new_data.attrs['Description'] = ' monthly mean values '
    if show_newPer=='YES':
        print('There are ' + str(new_data.time.values.size) + ' time steps')
        print('The first time stemp is : ' + str(new_data.time.values[0]))
        print('The second time stemp is : ' + str(new_data.time.values[1]))
        print('The last time stemp is : ' + str(new_data.time.values[-1]))

    if save_nerCDF!='NO':
        new_data.to_netcdf(save_nerCDF)
    return new_data

