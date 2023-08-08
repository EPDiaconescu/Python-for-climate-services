import time
import xarray
import matplotlib.pyplot as plt
import glob, os

def Kelvin_to_Celsius(file, var, save='NO', figure='YES'):
    """ This function transforms Kelvin in Celsius for a netCDF file and save the new file as netCDF
	file = put here the path and the name of the netCDF file in Kelvin
	var = put here the name of the variable you want to change from Kelvin to Celsius
	save = if you want to save the file put here the path and the name of the netCDF file in Celsius; 
	if you don't want to save it, put 'NO' and use the file locally for other operations
	figure = put 'YES' if want to see a figure with the mean over the entire period.
    """
    ds = xarray.open_dataset(file)
    data_Celsius= ds[var]- 273.15
    if save!='NO':
        ds[var]= data_Celsius
        ds[var].attrs['Description'] = var+' expressed in Celsius'
        ds[var].attrs["units"] = "degrees_Celsius"
        ds.to_netcdf(save)
    if figure=='YES':
        fig1 = plt.figure()
        data_Celsius.mean(dim='time').plot.contourf(x='lon', y='lat', cmap='BrBG_r', levels=22)
        plt.show()
    return data_Celsius



############## EXAMPLE 2 ################################
# the following script will transform all the files that are in the directory indicated in input and save them in output
input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas and are ended with .nc
list=glob.glob('tas_hist*.nc')

# we construct a loop, which will call the function for each files we put in the list

for fld in list[:]:
    print(fld)
    fileout = fld[:-3] + '_Celsius.nc'
    Kelvin_to_Celsius(input+fld, 'tas', save=output+fileout, figure='NO')
