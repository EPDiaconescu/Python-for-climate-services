import numpy as np
import pandas as pd
import xclim.indices as indices
import xarray as xr
import matplotlib.pyplot as plt

"""This script will compute 1 annual precipitation index:
    a) annual sum of days with pr > 50 mm
Missing values follows 3/5 rule, in addition to which 90% of years must be present to compute index (3/5 rule needs verification)
    """

input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/Climate Data Requests Input Data/'
#output='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/Climate Data Requests Output Data/'
data_df = pd.read_csv(input + 'OttawaIntlAirportA.csv', header=0, parse_dates=True, squeeze=True)

station='Ottawa Intl Airport A'
province='ON'
index='pr_50'
index_name='Heavy Precipitation'
#thresh='25'
freq='Annual'
units='mm/d'
ylabel='Annual Sum for Days with pr > 50mm'
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
    stacked_years=stacked_years.set_index('time')
    
    #####################NEW DF#######################################
    years4= [g for n, g in stacked_years.set_index(stacked_years.index).groupby(pd.TimeGrouper('Y'))]
        
    #calc 1:
    list_greater=[]
    for i in years4:
        count= i['TOTAL_PRECIPITATION'][i['TOTAL_PRECIPITATION'] > 50.0].count()
        list_greater.append(count)    

    # calc 2:
    list_sum=[]
    for i in years4:
        count2=round(i['TOTAL_PRECIPITATION'][i['TOTAL_PRECIPITATION'] > 50.0].sum())
        list_sum.append(count2)
        
    years=np.arange(1898,2005,1)   
    years=years.tolist()
        
    #setting up final DF:
    df_final=pd.DataFrame(index=years)
    df_final['count']=list_greater
    df_final['sum']=list_sum
    
    

##########STEP 7-PLOTTING###################################################################
    plt.figure(figsize=(10,7))
    #y1=df_final['count']
    y2=df_final['sum']
    q=np.arange(1900,2010,10)
    x=df_final.index
    plt.xlabel(xlabel, size=20)
    plt.ylabel(ylabel, size=20)#freq+ index_name +' (mm)', size=20)#+ '(>'+thresh+'mm', size=20)
    plt.title(index_name+'-'+station +', '+str(first_year)+'-'+str(last_year),size=20)
    #plt.plot(x, y)
    plt.bar(x,y2)
    plt.legend()
    plt.xticks(q,size=15)
    #plt.yticks([1,2,3,4],size=20)
    plt.yticks(size=15)    
    plt.savefig(output+ index +'_SUM'+ station +'.png', dpi=400,  bbox_inches = 'tight')

##########################################################################    
    

except Exception as e:
    print(str(e))
    print('No data for this station')
