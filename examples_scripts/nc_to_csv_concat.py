import pandas as pd
import xarray
import glob, os
import numpy as np

input='C:/Users/pomeroyc/Desktop/nctocsv/'
output='C:/Users/pomeroyc/Desktop/nctocsv/csv/'

# Change directory to input
os.chdir(input)
rcps = ['rcp26', 'rcp45', 'rcp85']
# change to varname found in netcdf (normally shown in filename)
varName='heat_wave_frequency'



###############################################################################################
# list all files in your folder that end in  .nc
for r in rcps:
    list=glob.glob('*'+r+'*.nc')
#empty dataframe to fill
    allmodels = pd.DataFrame()
    
    for x in list:
        new_csv = x[0:43]  + '.csv'
        model_name = str(x).split("_")[-5]
        ds = xarray.open_dataset(input+x)
        YYstring=pd.Series(ds['time.year'].values)
        values=pd.Series(ds[varName].values.flatten())
        if len(values) != 151:
            values = values.append(pd.Series(np.nan))
            YYstring = YYstring.append(pd.Series(2100))
            YYstring.index = YYstring
            values.index = YYstring
        else:
            values = values
        table = pd.concat( [YYstring, values], axis=1)
        table.columns=['Year', model_name]
        allmodels[model_name] = table[model_name].values
    allmodels.index = YYstring
    allmodelsq = allmodels
    allmodels['p10'] = allmodelsq.quantile(q=0.1, axis = 1)
    allmodels['Median'] = allmodelsq.quantile(q=0.5, axis = 1)
    allmodels['p90'] = allmodelsq.quantile(q=0.9, axis = 1)
    allmodels.to_csv(output+r+new_csv, sep=',',index=True)
	

################################



