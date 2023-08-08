import pandas as pd
import xarray
import glob, os


input='C:/Users/pomeroyc/Desktop/nctocsv/'
output='C:/Users/pomeroyc/Desktop/nctocsv/csv/'

# Change directory to input
os.chdir(input)

# list all files in your folder that end in  .nc
list=glob.glob('*.nc')
# change to varname found in netcdf (normally shown in filename)
varName='heat_wave_frequency'

###############################################################################################
for x in list:
    new_csv = x[0:-3]  + '.csv'
    ds = xarray.open_dataset(input+x)
    YYstring=pd.Series(ds['time.year'].values)
    #MMstring=pd.Series(ds['time.month'].values)
    #DDstring=pd.Series(ds['time.day'].values)
    values=pd.Series(ds[varName].values.flatten())
    table = pd.concat( [YYstring, values], axis=1)
    table.columns=['Year', varName]
    table.index = YYstring
    table.to_csv(output+new_csv, sep=',',index=False)
	

################################



