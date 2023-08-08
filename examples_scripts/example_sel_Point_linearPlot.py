import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt

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
    lat_v =dataSel.lat.values
    lon_v=dataSel.lon.values
    timestring = pd.Series(t.strftime('%Y-%m-%d'))
    YYstring = pd.Series(t.strftime('%Y'))
    MMstring = pd.Series(t.strftime('%m'))
    DDstring = pd.Series(t.strftime('%d'))
    values=pd.Series(dataSel.values)
    table2= pd.DataFrame(dataSel.values, index=timestring, columns=[var])
    table = pd.concat( [timestring, YYstring, MMstring, DDstring, values], axis=1)
    table.columns=['date', 'year', 'month', 'day', var]


    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',',index=False)

    if save_nerCDF!='NO':
        dataSel.to_netcdf(save_nerCDF)
    return table2

################### EXAMPLE ##############

start = time.time()

###########################################
per='DJF'
var='sic'
latitude, longitude = 57.5, 275.5

input_histo= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_hist/'
output='G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

output_histo=output+var+'_absolute_ts_'+per+'_histo_lat57.5lon275.5.png'

fld_histo_pctl5=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl5_1900_2005.nc'
fld_histo_pctl25=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl25_1900_2005.nc'
fld_histo_pctl50=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl50_1900_2005.nc'
fld_histo_pctl75=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl75_1900_2005.nc'
fld_histo_pctl95=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl95_1900_2005.nc'


ch_histo_pctl5=selPoint(fld_histo_pctl5, var, latitude, longitude, save_nerCDF='NO',save_CSV=output+var+'_absolute_ts_'+per+'_histo_pctl5_lat57.5lon275.5.csv')
ch_histo_pctl25=selPoint(fld_histo_pctl25,var, latitude, longitude, save_nerCDF='NO',save_CSV=output+var+'_absolute_ts_'+per+'_histo_pctl25_lat57.5lon275.5.csv')
ch_histo_pctl50=selPoint(fld_histo_pctl50,var, latitude, longitude, save_nerCDF='NO',save_CSV=output+var+'_absolute_ts_'+per+'_histo_pctl50_lat57.5lon275.5.csv')
ch_histo_pctl75=selPoint(fld_histo_pctl75,var, latitude, longitude, save_nerCDF='NO',save_CSV=output+var+'_absolute_ts_'+per+'_histo_pctl75_lat57.5lon275.5.csv')
ch_histo_pctl95=selPoint(fld_histo_pctl95,var, latitude, longitude, save_nerCDF='NO',save_CSV=output+var+'_absolute_ts_'+per+'_histo_pctl95_lat57.5lon275.5.csv')

table=pd.concat( [ch_histo_pctl5, ch_histo_pctl25, ch_histo_pctl50, ch_histo_pctl75, ch_histo_pctl95], axis=1)
table.columns=['pctl_5','pctl_25','pctl_50','pctl_75','pctl_95']
table.plot(figsize=(16,8),title=var+' '+per+' lat = '+latitude+' lon = '+longitude,style=['-','--','-','--','-'])
plt.savefig(output_histo)

input_rcp26= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_rcp26/'
output_rcp26=output+var+'_absolute_ts_'+per+'_rcp26_lat57.5lon275.5.png'

fld_rcp26_pctl5=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl5_2006_2100.nc'
fld_rcp26_pctl25=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl25_2006_2100.nc'
fld_rcp26_pctl50=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl50_2006_2100.nc'
fld_rcp26_pctl75=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl75_2006_2100.nc'
fld_rcp26_pctl95=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl95_2006_2100.nc'

ch_rcp26_pctl5=selPoint(fld_rcp26_pctl5,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp26_pctl25=selPoint(fld_rcp26_pctl25,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp26_pctl50=selPoint(fld_rcp26_pctl50,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp26_pctl75=selPoint(fld_rcp26_pctl75,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp26_pctl95=selPoint(fld_rcp26_pctl95,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')

table_rcp26=pd.concat( [ch_rcp26_pctl5, ch_rcp26_pctl25, ch_rcp26_pctl50, ch_rcp26_pctl75, ch_rcp26_pctl95], axis=1)
table_rcp26.columns=['pctl_5','pctl_25','pctl_50','pctl_75','pctl_95']
table_rcp26.plot(figsize=(16,8),title=var+' '+per+' lat = '+latitude+' lon = '+longitude,style=['-','--','-','--','-'])
plt.savefig(output_rcp26)


input_rcp45= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_rcp45/'
output_rcp45=output+var+'_absolute_ts_'+per+'_rcp45_lat57.5lon275.5.png'

fld_rcp45_pctl5=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl5_2006_2100.nc'
fld_rcp45_pctl25=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl25_2006_2100.nc'
fld_rcp45_pctl50=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl50_2006_2100.nc'
fld_rcp45_pctl75=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl75_2006_2100.nc'
fld_rcp45_pctl95=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl95_2006_2100.nc'

ch_rcp45_pctl5=selPoint(fld_rcp45_pctl5,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp45_pctl25=selPoint(fld_rcp45_pctl25,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp45_pctl50=selPoint(fld_rcp45_pctl50,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp45_pctl75=selPoint(fld_rcp45_pctl75,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp45_pctl95=selPoint(fld_rcp45_pctl95,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')

table_rcp45=pd.concat( [ch_rcp45_pctl5, ch_rcp45_pctl25, ch_rcp45_pctl50, ch_rcp45_pctl75, ch_rcp45_pctl95], axis=1)
table_rcp45.columns=['pctl_5','pctl_25','pctl_50','pctl_75','pctl_95']
table_rcp45.plot(figsize=(16,8),title=var+' '+per+' lat = '+latitude+' lon = '+longitude,style=['-','--','-','--','-'])
plt.savefig(output_rcp45)

input_rcp85= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_rcp85/'
output_rcp85=output+var+'_absolute_ts_'+per+'_rcp85_lat57.5lon275.5.png'

fld_rcp85_pctl5=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl5_2006_2100.nc'
fld_rcp85_pctl25=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl25_2006_2100.nc'
fld_rcp85_pctl50=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl50_2006_2100.nc'
fld_rcp85_pctl75=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl75_2006_2100.nc'
fld_rcp85_pctl95=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl95_2006_2100.nc'

ch_rcp85_pctl5=selPoint(fld_rcp85_pctl5,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp85_pctl25=selPoint(fld_rcp85_pctl25,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp85_pctl50=selPoint(fld_rcp85_pctl50,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp85_pctl75=selPoint(fld_rcp85_pctl75,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')
ch_rcp85_pctl95=selPoint(fld_rcp85_pctl95,var, latitude, longitude, save_nerCDF='NO',save_CSV='NO')

table_rcp85=pd.concat( [ch_rcp85_pctl5, ch_rcp85_pctl25, ch_rcp85_pctl50, ch_rcp85_pctl75, ch_rcp85_pctl95], axis=1)
table_rcp85.columns=['pctl_5','pctl_25','pctl_50','pctl_75','pctl_95']
table_rcp85.plot(figsize=(16,8),title=var+' '+per+' lat = '+latitude+' lon = '+longitude,style=['-','--','-','--','-'])
plt.savefig(output_rcp85)

#####################################

print('It took', time.time()-start, 'seconds.')
