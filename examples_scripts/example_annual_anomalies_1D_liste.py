import time
import pandas as pd
import xarray
import glob, os
start = time.time()

input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begins with tas_hist and is ended with .nc
liste=glob.glob('a_tas*.nc')
varName='tas'
#Put here the first and last year of the desired reference period
first_year= '1980'
last_year= '2005'

# Put here the name of the CSV file
new_fld = 'test_anomalies.csv'

NewDict=[]
for fld, nr in zip(liste, range(1, len(liste) + 1)):
    print (fld, 'm' + str(nr))
    nameModel = 'm' + str(nr)
    ds = xarray.open_dataset(input+fld, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    new_data = ds.resample(time='AS').mean('time')
    ref_data = ds.sel(time=slice(first_year, last_year))
    ref_mean = ref_data.mean('time')
    annual_anomalies = new_data - ref_mean
    annual_anomalies=annual_anomalies.rename({varName: nameModel}) 

    NewDict.append( annual_anomalies )
Final_xarray=xarray.merge(NewDict)
Final_table=Final_xarray.to_dataframe()

(Final_table.drop(['lon', 'lat'], axis=1)).plot()

print('It took', time.time()-start, 'seconds.')




