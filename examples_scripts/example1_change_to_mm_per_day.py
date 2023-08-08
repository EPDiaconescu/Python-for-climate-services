import xarray
import matplotlib.pyplot as plt
import time
import glob, os

def change_to_mm_per_day(file, var, save='NO', figure='YES'):
    """ This function transforms kg m-2 s-1 in mm/day for a netCDF file and save the new file as netCDF
	file = put here the path and the name of the netCDF file in kg m-2 s-1
	var = put here the name of the variable you want to change from kg m-2 s-1 to mm/day
	save = if you want to save the file put here the path and the name of the netCDF file in mm/day; if you don't want to save it, put 'NO' and use the file locally for other operations
	figure = put 'YES' if want to see a figure with the mean over the entire period.
    """
    ds = xarray.open_dataset(file)
    data_mmday= ds[var]*86400
    if save!='NO':
        ds[var]= data_mmday
        ds[var].attrs['Description'] = var+' expressed in mm/day'
        ds[var].attrs["units"] = "mm/day"
        ds.to_netcdf(save)
    if figure=='YES':
        fig1 = plt.figure()
        data_mmday.mean(dim='time').plot.contourf(x='lon', y='lat', cmap='BrBG_r', levels=22)
        plt.show()
    return data_mmday

################ EXAMPLE 1 #######################
#we start a chronometer
start = time.time()


# Put in input the path to the netCDF file you want to analyze
input= 'G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output= 'G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# we put here the name of the netCDF file in kg m-2 s-1
fld='pre_hist_canesm2_mm.nc'

# we put here the name of the final file in mm/day to save in output folder
# here I choose to use the same name as the initial file and to replace the last 3 characters of the name with _mmday.nc
fileout=fld[:-3]+'_mmday.nc'

# I will use the following line if I want just to see a rapid figure and not save the file but to have it on python
# for further operations (it will be the dataC variable)
dataC=change_to_mm_per_day(input+fld, 'pr', save='NO', figure='YES')

# I will use the following line if I want to save the new file as netCDF without seeing a figure
change_to_mm_per_day(input+fld, 'pr', save=output+fileout, figure='NO')

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')

