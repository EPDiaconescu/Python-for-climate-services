import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt

def spatial_mean(file,var, save_CSV='NO'):
    """ This function will open a netcDF file, make a area-weighted averages of gridded spatial data and save the new file. 
	The function supposes that the file has the spatial dimensions noted with lat and lon.
	file = put here the path and the name of the original netCDF file
	var = put here the name of the variable, ex. 'tas'
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    dataSel = ds[var]
    lonsM, latsM = np.meshgrid(dataSel.lon.values, dataSel.lat.values)
    wgtmat = np.cos(np.deg2rad(latsM))
    mean_Var = np.zeros(dataSel.time.size)  # Preallocation
    for i in range(dataSel.time.size):
        mean_Var[i] = (dataSel.values[i] * wgtmat).sum() / (wgtmat).sum()

    t = pd.to_datetime(dataSel.time.values)
    timestring = t.strftime('%Y-%m-%d')
    table = pd.DataFrame(mean_Var, index=timestring, columns=['Mean'])

    if save_CSV!='NO':
        table.to_csv(save_CSV, sep=',')
    return table
################### EXAMPLE ##############

start = time.time()

###########################################
# Put in input the path and the netCDF file you want
# Put in output the path and the name of the file you want to create
per='DJF'
var='sic'

output='E:/ec2018/work/2018summer-CMIP5/'+var+'_absolute_ts_'+per+'_spatialMean.png'


input_histo= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_hist/'
input_rcp26= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_rcp26/'
input_rcp45= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_rcp45/'
input_rcp85= 'Z:/CMIP5/CMIP5_files/sea_ice_concentration_rerun/'+var+'_absolute_ts/'+var+'_abs_ts_rcp85/'


fld_histo_pctl5=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl5_1900_2005.nc'
fld_histo_pctl25=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl25_1900_2005.nc'
fld_histo_pctl50=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl50_1900_2005.nc'
fld_histo_pctl75=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl75_1900_2005.nc'
fld_histo_pctl95=input_histo+var+'_OImon_ensABSts_historical_'+per+'_pctl95_1900_2005.nc'

fld_rcp26_pctl5=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl5_2006_2100.nc'
fld_rcp26_pctl25=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl25_2006_2100.nc'
fld_rcp26_pctl50=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl50_2006_2100.nc'
fld_rcp26_pctl75=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl75_2006_2100.nc'
fld_rcp26_pctl95=input_rcp26+var+'_OImon_ensABSts_rcp26_'+per+'_pctl95_2006_2100.nc'

fld_rcp45_pctl5=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl5_2006_2100.nc'
fld_rcp45_pctl25=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl25_2006_2100.nc'
fld_rcp45_pctl50=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl50_2006_2100.nc'
fld_rcp45_pctl75=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl75_2006_2100.nc'
fld_rcp45_pctl95=input_rcp45+var+'_OImon_ensABSts_rcp45_'+per+'_pctl95_2006_2100.nc'

fld_rcp85_pctl5=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl5_2006_2100.nc'
fld_rcp85_pctl25=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl25_2006_2100.nc'
fld_rcp85_pctl50=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl50_2006_2100.nc'
fld_rcp85_pctl75=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl75_2006_2100.nc'
fld_rcp85_pctl95=input_rcp85+var+'_OImon_ensABSts_rcp85_'+per+'_pctl95_2006_2100.nc'


ch_histo_pctl5=spatial_mean(fld_histo_pctl5,var, save_CSV='NO')
ch_histo_pctl25=spatial_mean(fld_histo_pctl25,var, save_CSV='NO')
ch_histo_pctl50=spatial_mean(fld_histo_pctl50,var, save_CSV='NO')
ch_histo_pctl75=spatial_mean(fld_histo_pctl75,var, save_CSV='NO')
ch_histo_pctl95=spatial_mean(fld_histo_pctl95,var, save_CSV='NO')

ch_rcp26_pctl5=spatial_mean(fld_rcp26_pctl5,var, save_CSV='NO')
ch_rcp26_pctl25=spatial_mean(fld_rcp26_pctl25,var, save_CSV='NO')
ch_rcp26_pctl50=spatial_mean(fld_rcp26_pctl50,var, save_CSV='NO')
ch_rcp26_pctl75=spatial_mean(fld_rcp26_pctl75,var, save_CSV='NO')
ch_rcp26_pctl95=spatial_mean(fld_rcp26_pctl95,var, save_CSV='NO')

ch_rcp45_pctl5=spatial_mean(fld_rcp45_pctl5,var, save_CSV='NO')
ch_rcp45_pctl25=spatial_mean(fld_rcp45_pctl25,var, save_CSV='NO')
ch_rcp45_pctl50=spatial_mean(fld_rcp45_pctl50,var, save_CSV='NO')
ch_rcp45_pctl75=spatial_mean(fld_rcp45_pctl75,var, save_CSV='NO')
ch_rcp45_pctl95=spatial_mean(fld_rcp45_pctl95,var, save_CSV='NO')

ch_rcp85_pctl5=spatial_mean(fld_rcp85_pctl5,var, save_CSV='NO')
ch_rcp85_pctl25=spatial_mean(fld_rcp85_pctl25,var, save_CSV='NO')
ch_rcp85_pctl50=spatial_mean(fld_rcp85_pctl50,var, save_CSV='NO')
ch_rcp85_pctl75=spatial_mean(fld_rcp85_pctl75,var, save_CSV='NO')
ch_rcp85_pctl95=spatial_mean(fld_rcp85_pctl95,var, save_CSV='NO')

fig = plt.figure(figsize=(16,8))

plt.axhline(linewidth=1.0, ls='--', color='k')


plt.plot((ch_histo_pctl50).index.tolist(), ch_histo_pctl50, 'k-', linewidth=2)
plt.plot((ch_rcp85_pctl50).index.tolist(), ch_rcp85_pctl50, 'r-', linewidth=2)
plt.plot((ch_rcp45_pctl50).index.tolist(), ch_rcp45_pctl50, color='orange',linestyle='-', linewidth=2)
plt.plot((ch_rcp26_pctl50).index.tolist(), ch_rcp26_pctl50, 'b-', linewidth=2)

plt.plot((ch_histo_pctl25).index.tolist(), ch_histo_pctl25, 'k--', linewidth=1)
plt.plot((ch_rcp85_pctl25).index.tolist(), ch_rcp85_pctl25, 'r--', linewidth=1)
plt.plot((ch_rcp45_pctl25).index.tolist(), ch_rcp45_pctl25, color='orange',linestyle='--', linewidth=1)
plt.plot((ch_rcp26_pctl25).index.tolist(), ch_rcp26_pctl25, 'b--', linewidth=1)

plt.plot((ch_histo_pctl75).index.tolist(), ch_histo_pctl75, 'k--', linewidth=1)
plt.plot((ch_rcp85_pctl75).index.tolist(), ch_rcp85_pctl75, 'r--', linewidth=1)
plt.plot((ch_rcp45_pctl75).index.tolist(), ch_rcp45_pctl75, color='orange',linestyle='--', linewidth=1)
plt.plot((ch_rcp26_pctl75).index.tolist(), ch_rcp26_pctl75, 'b--', linewidth=1)

plt.plot((ch_histo_pctl5).index.tolist(), ch_histo_pctl5, 'k:', linewidth=1)
plt.plot((ch_rcp85_pctl5).index.tolist(), ch_rcp85_pctl5, 'r:', linewidth=1)
plt.plot((ch_rcp45_pctl5).index.tolist(), ch_rcp45_pctl5, color='orange',linestyle=':', linewidth=1)
plt.plot((ch_rcp26_pctl5).index.tolist(), ch_rcp26_pctl5, 'b:', linewidth=1)

plt.plot((ch_histo_pctl95).index.tolist(), ch_histo_pctl95, 'k:', linewidth=1)
plt.plot((ch_rcp85_pctl95).index.tolist(), ch_rcp85_pctl95, 'r:', linewidth=1)
plt.plot((ch_rcp45_pctl95).index.tolist(), ch_rcp45_pctl95, color='orange',linestyle=':', linewidth=1)
plt.plot((ch_rcp26_pctl95).index.tolist(), ch_rcp26_pctl95, 'b:', linewidth=1)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

#plt.ylabel(labelYY, fontsize=10)
plt.xlabel('Year', fontsize=10)
#plt.title(labelUp, fontsize=16)

#plt.ylim(ylmi, ylma)

#fig.autofmt_xdate()
plt.savefig(output)

#####################################

print('It took', time.time()-start, 'seconds.')
