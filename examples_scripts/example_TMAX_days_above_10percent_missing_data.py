import numpy as np
import pandas as pd
import xclim.indices as indices
import xarray as xr
import matplotlib.pyplot as plt

input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/Climate Data Requests Input Data/'
#output='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/Climate Data Requests Output Data/'
data_df = pd.read_csv(input + 'moncton.csv', header=0, parse_dates=True, squeeze=True)

station='Moncton, NB 8103100'
index='tx_max'
index_name='Summer Days'
Thresh='30 degC'
freq='Annual'
units='degC'
ylabel='Number of days above 30°C'
xlabel='Year'
first_year=1898
last_year=2004
var_name='MAX_TEMPERATURE'
index_name='Days with TMAX greater than 30'

##############################

data_df=data_df[['LOCAL_DATE',var_name]]
data_df.columns=['time',var_name]
data_df=data_df.set_index('time')
data_df.index=pd.to_datetime(data_df.index)
data_df=data_df.reset_index()


data_df = data_df.set_index('time').fillna(np.nan).rename_axis('time').reset_index()


t = pd.to_datetime(data_df.index)
MMstring = pd.Series(t.strftime('%m'))
DDstring = pd.Series(t.strftime('%d'))
df=pd.concat([MMstring, DDstring,data_df],axis=1)
df=df.set_index('time')
df.columns=['Month','Day',var_name]

index_all=[]

years= [g for n, g in df.set_index(df.index).groupby(pd.TimeGrouper('Y'))]
for i in years:
    print('number missing days:', i[var_name].isna().sum())
    if i[var_name].isna().sum() < 36: 
        xds = xr.Dataset.from_dataframe(i)
        ###ERRROR!!!!!!#########
        xds_da=xds[var_name]
        xds_da.attrs['units'] = units
        tout=indices.tx_days_above(xds_da, thresh= Thresh)
        index_all.append(tout)
    else:
        
        tout = xr.Dataset.from_dataframe(pd.DataFrame([np.nan],columns=[var_name], index=[i.index[0]]))
        tout=tout.rename({'index': 'time'})
        index_all.append(tout)
 
index_final=xr.merge(index_all)   
index_final=index_final.rename({var_name: index_name})   
   
index_final[index_name].plot()        

#plt.savefig(output+ index +'_'+thresh+'_'+ station +'.png', dpi=400,  bbox_inches = 'tight')




        