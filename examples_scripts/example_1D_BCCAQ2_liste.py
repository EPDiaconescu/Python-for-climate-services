import time
import pandas as pd
import xarray
import glob, os

################ EXAMPLE #######################
#we start a chronometer
start = time.time()

input='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/dataReq1/'
output='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Data/dataReq1/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas_hist and are ended with .nc
list=glob.glob('tasmin_*rcp85_r1i1p1_lon-83.0364_lat42.3149.nc')
varName='tasmin'

# Put here the name of the CSV file
new_fld = 'tasmin_BCCAQ2_rcp85_1D_lon-83.0364_lat42.3149.csv'

fld = list[:1][0]
ds = xarray.open_dataset(input+fld, decode_times=False)
ds['time'] = xarray.decode_cf(ds).time
t = pd.to_datetime(ds.time.values)
timestring = pd.Series(t.strftime('%Y-%m-%d'))
YYstring = pd.Series(t.strftime('%Y'))
values=pd.Series(ds[varName].values.flatten())
table = pd.concat( [timestring, values], axis=1)
table.columns=['time', 'm1']
table.index = timestring
print (fld, 'm1')
for fld, nr in zip(list[1:], range(2, len(list) + 2)):
    nameModel = 'm' + str(nr)
    ds = xarray.open_dataset(input+fld, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    t = pd.to_datetime(ds.time.values)
    timestring = pd.Series(t.strftime('%Y-%m-%d'))
    table[nameModel] = pd.DataFrame(ds[varName].values.flatten(), index=timestring, columns=[nameModel])
	
#table.to_csv(output+new_fld, sep=',',index=False)

print('It took', time.time()-start, 'seconds.')

table.isna().sum()
################################



