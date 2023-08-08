import time
import pandas as pd
import xarray


def selPoint(file, var, latitude, longitude, save_nerCDF='NO',save_CSV='NO'):
    """ This function will open a netcDF file, select data for the grid point situated closest 
	to latitude and longitude indicated and save the new file in netCDF or CSV.
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	file = put here the path and the name of the original netCDF file
	var = put here the name of the variable, ex. 'tas'
	latitude, longitude= put here the approximative coordinates of the point
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save;  
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    dataSel = ds[var].sel(lat=latitude, lon=longitude, method='nearest')
    YYstring=pd.Series(ds['time.year'].values)
    MMstring=pd.Series(ds['time.year'].values)
    DDstring=pd.Series(ds['time.year'].values)
    values=pd.Series(dataSel.values)
    table = pd.concat( [YYstring, MMstring, DDstring, values], axis=1)
    table.columns=['year', 'month', 'day', var]


    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',',index=False)

    if save_nerCDF!='NO':
        dataSel.to_netcdf(save_nerCDF)
    
    return table

################ EXAMPLE 1 #######################
#we start a chronometer
start = time.time()

#put here the approximative coordinates of the point
latitude=45.5
longitude= 360.0-75.7

# Put in input the path to the folder with the netCDF file you want
input='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# Put here the name of the netCDF file
fld='tas_hist_gisse2r.nc'

# Put in output the path to the folder where you want to save the files
output='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# put here the name of the new netCDF file
new_netCDF=fld[:-3] + '_lat'+str(latitude)+'_lon'+str(longitude)+'.nc'
# put here the name of the new csv file
new_csv=fld[:-3] + '_lat'+str(latitude)+'_lon'+str(longitude)+'.csv'

# Put here the name of the netCDF variable
var='tas'

#apply the function
dataS=selPoint(input+fld, var, latitude, longitude, save_nerCDF=output+new_netCDF,save_CSV=output+new_csv)

# if we want a quick plot of the data in the point
#dataS.index=dataS['date']
# dataS[var].plot()

# if we want to have a quick view of the new data:
# dataS

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')


