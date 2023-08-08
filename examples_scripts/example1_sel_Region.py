import time
import xarray

def sel_Region(file, lat_bottom, lat_top, lon_left, lon_right, show_regInfo='YES', save_nerCDF='NO'):
    """ This function will open a netcDF file, select data situated into a rectangle defined by the closest points 
	to lat_bottom, lat_top, lon_left, lon_right, and save the new file in netCDF. 
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	file = put here the path and the name of the original netCDF file
	lat_bottom, lat_top, lon_left, lon_right= put here the approximative coordinates of the region
	show_newPer= put 'YES' if you want to verify the lat and long selected
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    latB = ds.lat.sel(lat=lat_bottom, method='nearest', tolerance=5)
    latT = ds.lat.sel(lat=lat_top, method='nearest', tolerance=5)
    lonL = ds.lon.sel(lon=lon_left, method='nearest', tolerance=5)
    lonR = ds.lon.sel(lon=lon_right, method='nearest', tolerance=5)
    dataSel = ds.sel(lat=slice(latB.values, latT.values), lon=slice(lonL.values, lonR.values))
    if show_regInfo=='YES':
        print('There are ' + str(dataSel.lat.values.size) + ' grid points for latitudes')
        print('The first latitude is : ' + str(dataSel.lat.values[0]))
        print('The second latitude is : ' + str(dataSel.lat.values[1]))
        print('The last latitude is : ' + str(dataSel.lat.values[-1]))
        print('  ')
        print('There are ' + str(dataSel.lon.values.size) + ' grid points for longitude')
        print('The first longitude is : ' + str(dataSel.lon.values[0]))
        print('The second longitude is : ' + str(dataSel.lon.values[1]))
        print('The last longitude is : ' + str(dataSel.lon.values[-1]))
        print('  ')

    if save_nerCDF!='NO':
        dataSel.to_netcdf(save_nerCDF)
    return dataSel

################### EXAMPLE 1 ##############
#we start a chronometer
start = time.time()

# Put in input the path to the netCDF file you want
input= 'G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# Put here the name of the netCDF file
fld='tasmax_day_BCCAQ2_GFDL-ESM2G_20960101-21001231.nc'

# Put in output the path to the folder where you want to save the new file
output='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# put here the name of the new file
# Here I named it as the initial one + the new at the end
new_file=fld[:-3]+'_new.nc'

# Put here the corners of the region you want
# Attention aux longitude if expressed in values from -180 to 180 or from 0 to 360; use the format of your data
lat_bottom=35.0
lat_top=50.0
lon_left=360-85
lon_right=360-55

# we apply the function
dataS= sel_Region(input+fld, lat_top, lon_left, lon_right, show_regInfo='YES', save_nerCDF=output+new_file)

#####################################

print 'It took', time.time()-start, 'seconds.'
