import time
import pandas as pd
import xarray
import glob, os

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
    t = pd.to_datetime(dataSel.time.values)
    timestring = pd.Series(t.strftime('%Y-%m-%d'))
    YYstring = pd.Series(t.strftime('%Y'))
    MMstring = pd.Series(t.strftime('%m'))
    DDstring = pd.Series(t.strftime('%d'))
    values=pd.Series(dataSel.values)
    table = pd.concat( [timestring, YYstring, MMstring, DDstring, values], axis=1)
    table.columns=['date', 'year', 'month', 'day', var]


    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',',index=False)

    if save_nerCDF!='NO':
        dataSel.to_netcdf(save_nerCDF)
    return table

################ EXAMPLE 2 : several models saved separately #######################
#we start a chronometer
start = time.time()

#put here the approximative coordinates of the point
latitude=56.65333
longitude=360-111.22333

# Put in input the path to the folder with your netCDF files
input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/snd/Hist/'

# Put in output the path to the folder where you want to save the files
output='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/snd/test/'

# Put here the name of the netCDF variable
var='snd'

# first we go in the directory indicated in input
os.chdir(input)

# we want all historical files
# we construct a list containing all the file in this directory that begin with tas_hist and are ended with .nc
list=glob.glob('*.nc')

# we construct a loop, which will call the function for each files we put in the list
for fld in list[:]:
    print(fld)
    # put here the name of the new netCDF file
    new_netCDF = fld[:-3] + '_lat' + str(latitude) + '_lon' + str(longitude) + '.nc'
    # put here the name of the new csv file
    new_csv = fld[:-3] + '_lat' + str(latitude) + '_lon' + str(longitude) + '.csv'
    dataS = selPoint(input + fld, var, latitude, longitude, save_nerCDF=output+new_netCDF, save_CSV=output+new_csv)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
################################



