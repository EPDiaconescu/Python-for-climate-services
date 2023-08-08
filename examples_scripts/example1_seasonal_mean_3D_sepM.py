import time
import xarray
import glob, os

#####################################
def seasonal_mean_3D_sepM(file, save_nerCDF='NO'):
    """ This function will open an 3D netcDF file, compute the time mean for each season and save the new file in netCDF.
	The date indicated for each season is the last time step of the corresponding season.
	Each season will be saved in a separate file.
	file = put here the path and the name of the original netCDF file
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save without .nc
	(the program will add the seasons at the end of the name and the .nc)
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    new_data=ds.resample(time='Q-NOV').mean('time')
    new_data.attrs['Description'] = ' seasonal mean values '

    def is_winter(month):
        return (month >= 1) & (month <= 2)
    winter_data = new_data.sel(time=is_winter(new_data['time.month']))
    def is_spring(month):
        return (month >= 3) & (month <= 5)
    spring_data = new_data.sel(time=is_spring(new_data['time.month']))
    def is_summer(month):
        return (month >= 6) & (month <= 8)
    summer_data = new_data.sel(time=is_summer(new_data['time.month']))
    def is_autumn(month):
        return (month >= 9) & (month <= 11)
    autumn_data = new_data.sel(time=is_autumn(new_data['time.month']))

    if save_nerCDF!='NO':
        winter_data.to_netcdf(save_nerCDF+'_winter.nc')
        spring_data.to_netcdf(save_nerCDF+'_spring.nc')
        summer_data.to_netcdf(save_nerCDF+'_summer.nc')
        autumn_data.to_netcdf(save_nerCDF+'_autumn.nc')
    return winter_data, spring_data, summer_data, autumn_data

################### EXAMPLE ##############
#we start a chronometer
start = time.time()

# Put in input the path and the netCDF file you want
input= 'O:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/tas_hist_canesm2_mm.nc'

# Put in output the path and the name of the file you want to create
output='O:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/test_seasonal_mean.nc'

seasonal_mean_3D_sepM(input, save_nerCDF=output)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
