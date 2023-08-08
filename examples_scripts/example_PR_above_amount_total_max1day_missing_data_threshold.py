import numpy as np
import pandas as pd
import xclim.indices as indices
import xarray as xr
import matplotlib.pyplot as plt

"""This script will compute 3 annual precipitation indices separately:
    a) total annual precipitation
    b) max 1 day precipitation
    c) wet days (days with pr > 50 mm)
Missing values follows 3/5 rule, in addition to which 90% of years must be present to compute index (3/5 rule needs verification)
    """


input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/Climate Data Requests Input Data/'
#output='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/Climate Data Requests Output Data/'
data_df = pd.read_csv(input + 'moncton.csv', header=0, parse_dates=True, squeeze=True)

station='Moncton, NB 8103100'

province='NB'
index='pr_50'
index_name='Precipitation'
#thresh='25'
freq='Annual'
units='mm/d'
#ylabel='Total Precipitation (mm)'
ylabel='Days with Precipitation > 50mm'
#ylabel='Max 1 Day Precipitation (mm)'
xlabel='Year'
first_year=1898
last_year=2004

######### STEP 1-ADD IN MISSING DATES IN INDEX##########################################    
try: 
    data_df=data_df[['LOCAL_DATE','TOTAL_PRECIPITATION']]
    data_df.columns=['time','TOTAL_PRECIPITATION']
    
    
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
    df.columns=['Month','Day','TOTAL_PRECIPITATION']
    df.index=pd.to_datetime(df.index)
    
    
    #########STEP 2- THRESHOLD FOR MISSING VALUES##############################################
    #THRESHOLD: IF 3+ consecutive missing values in one month OR 5+ random missing values in one month
    # THEN entire year is set to missing
    
    months = [g for n, g in df.set_index(df.index).groupby(pd.TimeGrouper('M'))]
    
    good_months=[]
    for i in months:
        if i['TOTAL_PRECIPITATION'].isna().sum() <5 and (i['TOTAL_PRECIPITATION'].isnull().astype(int).groupby(i['TOTAL_PRECIPITATION'].notnull().astype(int).cumsum()).sum()  >= 3).any() != True: 
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
        xds_da=xds['TOTAL_PRECIPITATION']
        xds_da.attrs['units'] = units
       
        #choose index:
        #a) prout=indices.precip_accumulation(xds_da)             #Total Precipitation
        #b) prout=indices.max_1day_precipitation_amount(xds_da)   #Max 1-day Precipitation

        #c) 
        prout=indices.wetdays(xds_da, thresh='50.0mm/day')        #Days Above Precipitation Threshold
        values=prout.values
        values=values.astype('float')
        values[values== 0] = np.nan 
        print (prout)
        
    ##########STEP 6-NUMBER OF CONSECUTIVE YEARS###################################################################
        print (str(len(prout.time)) + ' years.')
    
    
    
    ##########STEP 7-PLOTTING###################################################################        
        years=np.arange(first_year,last_year+1,1)
        plt.figure(figsize=(10,7))
        y=values
        x=years
        plt.xlabel(xlabel, size=20)
        #plt.yticks(np.arange(0, 100, step=10), fontsize=60)                                                   
        plt.ylabel(ylabel, size=20)#freq+ index_name +' (mm)', size=20)#+ '(>'+thresh+'mm', size=20)
        plt.title(index_name+'-'+station +', '+str(first_year)+'-'+str(last_year),size=20)
        #plt.plot(x, y)
        plt.bar(x,y)
        plt.legend()
        z=np.arange(1,5,1).tolist()
        q=np.arange(1900,2010,10)
        plt.yticks(z,size=15)
        plt.xticks(q,size=15)
        
        plt.savefig(output +index +'_'+ station +'.png', dpi=400,  bbox_inches = 'tight')
    
    
    else:
          print('there is insufficient data for this station to compute index'+' ('+str(range)+'%).')
        
except Exception as e:
    print(str(e))
    print('No data for this station')