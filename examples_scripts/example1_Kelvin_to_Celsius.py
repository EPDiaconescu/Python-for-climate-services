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

################ EXAMPLE 1 #######################
#we start a chronometer
start = time.time()

# Put in input the path to the netCDF file you want to analyze
input= 'Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output= 'Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# we put here the name of the netCDF file in Kelvin
fld='tas_hist_gisse2h.nc'

# we put here the name of the final file in Celsius to save in output folder
# here I choose to use the same name as the initial file and to replace the last 3 characters of the name with _Celsius.nc
fileout=fld[:-3]+'_Celsius_Shawn.nc'

# I will use the following line if I want just to see a rapid figure and not save the file but to have it on python
# for further operations (it will be the dataC variable)
#dataC=Kelvin_to_Celsius(input+fld, 'tas', save='NO', figure='YES')

# I will use the following line if I want to save the new file as netCDF without seeing a figure
Kelvin_to_Celsius(input+fld, 'tas', save=output+fileout, figure='NO')

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')

