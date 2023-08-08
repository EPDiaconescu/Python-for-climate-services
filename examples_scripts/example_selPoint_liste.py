import time
import pandas as pd
import xarray
import glob, os

def selPoint_liste(input, liste, var, latitude, longitude, save_CSV='NO'):
    """ This function will open several netcDF files, for each of them will select data for
    the grid point situated closest to latitude and longitude indicated and save the information from all models in one csv
	input = put here the path to the netCDF files
	liste = put here the list with the names of all netCDF files you want
	var = put here the name of the variable, ex. 'tas'
	latitude, longitude= put here the approximative coordinates of the point
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations
    """
    fld = liste[:1][0]
    ds = xarray.open_dataset(input+fld, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    dataSel = ds[var].sel(lat=latitude, lon=longitude, method='nearest')
    #t = pd.to_datetime(dataSel.time.values)
    #timestring = pd.Series(t.strftime('%Y-%m-%d'))
    #YYstring = pd.Series(t.strftime('%Y'))
    #MMstring = pd.Series(t.strftime('%m'))
    #DDstring = pd.Series(t.strftime('%d'))
    YYstring=pd.Series(ds['time.year'].values)
    MMstring=pd.Series(ds['time.month'].values)
    DDstring=pd.Series(ds['time.day'].values)
    values=pd.Series(dataSel.values)
    table = pd.concat( [MMstring, DDstring, values], axis=1)
    table.columns=['month', 'day', 'm1']
    table.index = YYstring
    print (fld, 'm1')
    for fld, nr in zip(liste[1:], range(2, len(liste) + 2)):
        print (fld, 'm' + str(nr))
        nameModel = 'm' + str(nr)
        ds = xarray.open_dataset(input+fld)
        dataSel = ds[var].sel(lat=latitude, lon=longitude, method='nearest')
        YYstring=pd.Series(ds['time.year'].values)
        #t = pd.to_datetime(dataSel.time.values)
        #timestring = pd.Series(t.strftime('%Y-%m-%d'))
        table[nameModel] = pd.DataFrame(dataSel.values, index=YYstring, columns=[nameModel])

    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',',index=False)

    return table

################ EXAMPLE #######################
#we start a chronometer
start = time.time()

#put here the approximative coordinates of the point
latitude=45.5
longitude= 360.0-75.7

# Put here the name of the netCDF variable
var='tas'

# Put in input the path to the folder with your netCDF files
input='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'

# Put in output the path to the folder where you want to save the files
output='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# Put here the name of the CSV file
new_fld = 'CMIP5_histo_selection_lat'+str(latitude)+'_lon'+str(longitude)+'.csv'

# first we go in the directory indicated in input
os.chdir(input)

# we want all historical files
# we construct a list containing all the files in this directory that begin with tas_hist and are end with .nc
liste=glob.glob('tas_hist*.nc')

# we apply he function
newT=selPoint_liste(input, liste, var, latitude, longitude, save_CSV=output+new_fld)

#if you want to see the csv file in python : newT

# if we want a quick plot of the data from all models in the point
#(newT.drop(['year','month','day'], axis=1)).plot()

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
################################



