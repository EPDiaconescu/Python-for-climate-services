import numpy as np
import pandas as pd
import xclim.indices as indices
import xarray as xr
import matplotlib.pyplot as plt

"""This script will compute 2 annual tasmax indices separately:
    a) Number of days above 25°C
    b) Number of days above 30°C
Missing values follows 3/5 rule, in addition to which 90% of years must be present to compute index (3/5 rule needs verification)
    """

input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/Climate Data Requests Input Data/'
output='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/Climate Data Requests Output Data/'
data_df = pd.read_csv(input + 'moncton.csv', header=0, parse_dates=True, squeeze=True)

station='Moncton, NB 8103100'
index='tx_max'
index_name='Summer Days'
Thresh='25degC'
freq='Annual'
units='degC'
ylabel='Number of days above 25°C'
xlabel='Year'

first_year=1899
last_year=2004

######### STEP 1-ADD IN MISSING DATES IN INDEX##########################################
try:
    data_df=data_df[['LOCAL_DATE','MAX_TEMPERATURE']]
    data_df.columns=['time','MAX_TEMPERATURE']    
    data_df=data_df.reset_index()
    data_df = data_df.set_index('time').fillna(np.nan).rename_axis('time').reset_index()
    data_df=data_df.set_index('time')
    t = pd.to_datetime(data_df.index)
    MMstring = pd.Series(t.strftime('%m'))
    DDstring = pd.Series(t.strftime('%d'))
    data_df=data_df.reset_index()
    df=pd.concat([MMstring, DDstring,data_df],axis=1)
    df=df.drop(['index'],axis=1)
    df=df.set_index('time')
    df.columns=['Month','Day','MAX_TEMPERATURE']
    df.index=pd.to_datetime(df.index)
    
    
    #########STEP 2- THRESHOLD FOR MISSING VALUES##############################################
    #THRESHOLD: IF 3+ consecutive missing values in one month OR 5+ random missing values in one month
    # THEN entire year is set to missing
    
    months = [g for n, g in df.set_index(df.index).groupby(pd.TimeGrouper('M'))]
    
    good_months=[]
    for i in months:
        if i['MAX_TEMPERATURE'].isna().sum() <5 and (i['MAX_TEMPERATURE'].isnull().astype(int).groupby(i['MAX_TEMPERATURE'].notnull().astype(int).cumsum()).sum()  >= 3).any() != True: 
            good_months.append(i)
            
    stacked_months=pd.concat(good_months)
     
    good_years=[]
    years= [g for n, g in stacked_months.set_index(stacked_months.index).groupby(pd.TimeGrouper('Y'))]
    for i in years:
        if len(i) > 360:
            good_years.append(i)
                
    stacked_years=pd.concat(good_years)
    stacked_years=stacked_years.reset_index()
    
    ########STEP 3- ADD IN MISSING DATES IN NEW INDEX#######################################
    s = pd.date_range(start=stacked_years.time.min(), end=stacked_years.time.max())
    stacked_years_filled = stacked_years.set_index('time').reindex(s).fillna(np.nan).rename_axis('time').reset_index()
    stacked_years_filled=stacked_years_filled.set_index('time')
    stacked_years_filled=stacked_years_filled.drop(columns=['Month','Day'])
    
    
    ########STEP 4-CHECK FOR OVERALL % OF MISSING YEARS- RIGHT NOW AT 10% IS UPPER LIMIT##########
    range=round(len(stacked_years_filled) / len(df) * 100) 
    if range > 90:
        print(station +" has " +str(range) + " % " +"good data. yay." )
        
    ########STEP 5- COMPUTE INDEX IF SUFFICIENT DATA###########################################
        xds = xr.Dataset.from_dataframe(stacked_years_filled)
        xds_da=xds['MAX_TEMPERATURE']
        xds_da.attrs['units'] = units
        
        #choose index:
        #a) 
        tout=indices.tx_days_above(xds_da, thresh= Thresh)
        #b) tout=indices.tx_days_above(xds_da, thresh='30degC')        
        values=tout.values        
        values=values.astype('float')
        values[values== 0] = np.nan 
        print (tout)
        
    ##########STEP 6-NUMBER OF CONSECUTIVE YEARS###################################################################
        print (str(len(tout.time)) + ' years.')
        
    ##########STEP 7-PLOTTING###################################################################
        years=np.arange(first_year,last_year+1,1)
        plt.figure(figsize=(10,7))
        y=values
        x=years
        plt.xlabel(xlabel, size=20)
        plt.ylabel(ylabel, size=20)
        plt.title(index_name+'-'+station +', ' +str(first_year)+'-'+str(last_year),size=20)
        plt.plot(x, y)
        plt.legend()
        z=np.arange(5,25,5).tolist()
        q=np.arange(first_year, last_year,10)
        plt.xticks(q,size=15)
        plt.yticks(size=15)
        plt.savefig(output+ index +'_'+Thresh+'_'+ station +'.png', dpi=400,  bbox_inches = 'tight')
    
    
    else:
          print('there is insufficient data for this station to compute index.')
          
except Exception as e:
    print(str(e))
    print('No data for this station')
        