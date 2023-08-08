import time
import pandas as pd
import xarray
import glob, os

def annual_anomalies_1D_liste(input, liste, first_year, last_year,varName, save_CSV='NO'):
    """ This function will open several 1D netcDF files, for each of them will compute the anomalies
    for each year based on the selected reference period and save the all in one CSV.
    The date indicated for each year is the first time step of the corresponding year.
	input = put here the path to the original 1D netCDF file
	liste= indicate here the list of files
	first_year= put here the first year of the referene period
	last_year=put here the last year of the referenc period
	save_CSV= if you want to save the file put here the path and the name of the CSV file to save; 
	if you don't want to save it, put 'NO' and use the file locally for other operations
    """

    NewDict={}
    for fld, nr in zip(liste, range(1, len(liste) + 1)):
        print (fld, 'm' + str(nr))
        nameModel = 'm' + str(nr)
        ds = xarray.open_dataset(input+fld, decode_times=False)
        ds['time'] = xarray.decode_cf(ds).time
        new_data = ds.resample(time='AS').mean('time')
        ref_data = ds.sel(time=slice(first_year, last_year))
        ref_mean = ref_data.mean('time')
        annual_anomalies = new_data - ref_mean

        timestring =pd.to_datetime(pd.DataFrame({'year': annual_anomalies['time.year'].values,
                                                         'month': annual_anomalies['time.month'].values,
                                                         'day': annual_anomalies['time.day'].values}))

        table= pd.DataFrame(annual_anomalies[varName].values.flatten(), index=timestring, columns=[nameModel])
        NewDict.update( table )
    Final_table=pd.DataFrame.from_dict(NewDict)

    if save_CSV!='NO':
        Final_table.to_csv(save_CSV, sep=',',index=False)

    return Final_table

################ EXAMPLE #######################
#we start a chronometer
start = time.time()

input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

# first we go in the directory indicated in input
os.chdir(input)

# we construct now a list containing all the file in this directory that begin with tas_hist and are ended with .nc
list=glob.glob('a_tas*.nc')
varName='tas'
#Put here the first and last year of the desired reference period
first_year= '1980'
last_year= '2005'

# Put here the name of the CSV file
new_fld = 'test_anomalies.csv'


# we apply he function
newT=annual_anomalies_1D_liste(input, list, first_year, last_year, varName,save_CSV=output+new_fld)

newT.plot()

print('It took', time.time()-start, 'seconds.')
################################



