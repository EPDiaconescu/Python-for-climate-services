import time
import numpy as np
import pandas as pd
import xarray
import matplotlib.pyplot as plt
import glob,os


#####################################
def annual_anomalies_3D(file, first_year, last_year,project, rcp_name, varName,units,show_newPer='YES', save_nerCDF='NO'):
    """ This function will open an 3D netcDF file, compute the anomalies for each year based on the selected reference 
    period and save the new file in netCDF. The date indicated for each year is the first time step of the corresponding year.
	first_year= put here the first year of the reference period
	last_year=put here the last year of the reference period
	varName=name of the variable in the input files
	project= name of the project (ex: CMIP5 or BCCAQ2)
    rcp= the RCP for the scenario
    units= units of the variable of interest
	show_newPer= put 'YES' if you want to verify the time dimension information
	save_nerCDF= if you want to save the file put here the path and the name of the netCDF file to save;
	if you don't want to save it, put 'NO' and use the file locally for other operations.
    """
    ds=xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    new_data=ds.resample(time='AS').mean('time')
    ref_data=ds.sel(time=slice(first_year, last_year))
    ref_mean=ref_data.mean('time')
    annual_anomalies=new_data-ref_mean
    annual_anomalies.attrs['Description']='annual anomalies'
    annual_anomalies.attrs['CDI']=ds.attrs['CDI']
    annual_anomalies.attrs['Conventions']=ds.attrs['Conventions']
    annual_anomalies.attrs['project']=project
    annual_anomalies.attrs['experiment']=rcp_name
    annual_anomalies.attrs['GCM institute']=ds.attrs['institute_id']
    annual_anomalies.attrs['GCM']=ds.attrs['model_id']
    annual_anomalies[varName].attrs['standard_name']= ds[varName].attrs['long_name']
    annual_anomalies[varName].attrs['long_name']= ds[varName].attrs['long_name']
    annual_anomalies[varName].attrs['units']= units
    annual_anomalies[varName].attrs['frequency']= 'annual'
    if show_newPer=='YES':
        print('There are ' + str(new_data.time.values.size) + ' time steps')
        print('The first time stemp is : ' + str(new_data.time.values[0]))
        print('The second time stemp is : ' + str(new_data.time.values[1]))
        print('The last time stemp is : ' + str(new_data.time.values[-1]))
    if save_nerCDF!='NO':
        annual_anomalies.to_netcdf(save_nerCDF)
    return annual_anomalies
	
################### EXAMPLE ##############

start = time.time()

###########################################
# Put in input the path and the netCDF file you want

input='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/Temperature/'
output='H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5/Temperature/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas_hist and are ended with .nc
list=glob.glob('*tmean*.nc')

#Put here the first and last year of the desired reference period
first_year= '1986'
last_year= '2005'

# we construct a loop, which will call the function for each files we put in the list
for fld in list[:]:
    print(fld)
    fileout = fld[:-3] + '_anomalies.nc'
    annual_anomalies_3D(input + fld, first_year, last_year, 'CMIP5', 'RCP2.6','pr','mm/day', show_newPer='YES',
                        save_nerCDF=output + fileout)

# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')
