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


############## EXAMPLE 2 ################################
# the following script will transform all the files that are in the directory indicated in input and save them in output
input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with pre and are ended with .nc
list=glob.glob('pre*.nc')

# we construct a loop, which will call the function for each files we put in the list

for fld in list[:]:
    print(fld)
    fileout = fld[:-3] + '_mmday.nc'
    change_to_mm_per_day(input+fld, 'pr', save=output+fileout, figure='NO')
