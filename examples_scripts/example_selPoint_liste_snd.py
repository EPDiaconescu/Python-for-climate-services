import time
import pandas as pd
import xarray
import glob, os
import scipy.stats.mstats
import numpy as np

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
    t = pd.to_datetime(dataSel.time.values)
    timestring = pd.Series(t.strftime('%Y-%m-%d'))
    YYstring = pd.Series(t.strftime('%Y'))
    MMstring = pd.Series(t.strftime('%m'))
    DDstring = pd.Series(t.strftime('%d'))
    values=pd.Series(dataSel.values)
    table = pd.concat( [YYstring, MMstring, DDstring, values], axis=1)
    table.columns=['year', 'month', 'day', 'm1']
    table.index = timestring
    print (fld, 'm1')
    for fld, nr in zip(liste[1:], range(2, len(liste) + 2)):
        print (fld, 'm' + str(nr))
        nameModel = 'm' + str(nr)
        ds = xarray.open_dataset(input+fld, decode_times=False)
        ds['time'] = xarray.decode_cf(ds).time
        dataSel = ds[var].sel(lat=latitude, lon=longitude, method='nearest')
        t = pd.to_datetime(dataSel.time.values)
        timestring = pd.Series(t.strftime('%Y-%m-%d'))
        table[nameModel] = pd.DataFrame(dataSel.values, index=timestring, columns=[nameModel])

    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',',index=False)

    return table

################ EXAMPLE #######################
#we start a chronometer
start = time.time()

#put here the approximative coordinates of the point
latitude=56.65333
longitude=360-111.22333

# Put in input the path to the folder with your netCDF files
input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/snd/Hist/'

# Put here the name of the netCDF variable
var='snd'

#Put here the percentile you want to compute
percentiles=0.95

# Put in output the path to the folder where you want to save the files
output='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/snd/test/'

# Put here the name of the CSV file
new_fld = 'snd_CMIP5_histo_selection_lat'+str(latitude)+'_lon'+str(longitude)+'_allModels.csv'
new_fld2 = 'snd_CMIP5_histo_selection_lat'+str(latitude)+'_lon'+str(longitude)+'_p95.csv'

# first we go in the directory indicated in input
os.chdir(input)

# we want all historical files
# we construct a list containing all the files in this directory that begin with tas_hist and are end with .nc
liste=glob.glob('*.nc')

# we apply he function
newT=selPoint_liste(input, liste, var, latitude, longitude, save_CSV=output+new_fld)

newT2=newT.drop(['year', 'month','day'], axis=1)

QQ= []

for yy in newT2.index.tolist():
    print(yy)
    QQ=np.append(QQ,scipy.stats.mstats.mquantiles(newT2.loc[yy],prob=[percentiles],alphap=0.5,betap=0.5))

QQ_table=pd.DataFrame(QQ, index=newT2.index.tolist(),columns=['p_'+str(percentiles)])
#QQ2=pd.DataFrame(newT2.quantile(q=0.95, axis=1),columns=['p95'])
QQ_table.to_csv(output+new_fld2, sep=',')

#if you want to see the csv file in python : newT

# if we want a quick plot of the data from all models in the point
#(newT.drop(['year','month','day'], axis=1)).plot()

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
################################



