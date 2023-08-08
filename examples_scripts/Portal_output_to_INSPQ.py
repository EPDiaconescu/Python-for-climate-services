# -*- coding: utf-8 -*-
"""
This script converts the 30ymean_allmodels csv output from Travis's shapefile scripts into excel documents for each region and RCP
Each document has a sheet for each index
This script also calculates percentiles and appends them to the files
"""


import time 
import pandas as pd
from pandas import ExcelWriter
import xarray
import glob, os
import numpy as np



input='P:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/08 - Projects & Tasks/01 - DPO/INSPQ/OutputFinalZIP/'
outpath='C:/Users/pomeroyc/Desktop/INSPQ/HealthRegions/outpath/'
output='C:/Users/pomeroyc/Desktop/INSPQ/HealthRegions/output/'

# Change directory to input
os.chdir(input)
rcps = ['rcp45', 'rcp85']

indices= ['tx_max', 'tn_min', 'tg_mean', 'tn_mean', 'frost_days', 'ice_days',
          'tx_mean', 'tnlt_-15', 'tnlt_-25', 'txgt_25', 'txgt_30', 'txgt_32',
          'gddgrow_5', 'gddgrow_10', 'gddgrow_0', 'rx1day', 'r1mm', 'r10mm',
          'prcptot', 'tr_18', 'tr_20', 'cddcold_18', 'hddheat_17']

start = time.time()
mrcs = []
for r in rcps:
    for ind in indices:
        os.chdir(input+ind+'/'+r+'/YS/')
        list=glob.glob(ind+'*30y_Means_allModels*.csv')
        for g in list:
           #name of MRC
           mrcN=g.split("_")[-5]
           mrcs.append(mrcN)
           #open file
           w = pd.read_csv(g)
           #extract 3 time periods of interest
           w2 = w.iloc[[3,6,9],]
           #add percentiles at the end
           #ensure that data is in the right units
           w3 = w2.iloc[:,1:25]
           if ind == 'tn_min' or ind == 'tg_mean' or ind == 'tx_max' or ind == 'tx_mean' or ind == 'tn_mean':
                w2.iloc[:,1:25] = w3-273.15
                w2['p10'] = w3.quantile(q=0.1, axis = 1) - 273.15
                w2['Median'] = w3.quantile(q=0.5, axis = 1) - 273.15
                w2['p90'] = w3.quantile(q=0.9, axis = 1) - 273.15
           else:
                w2.iloc[:,1:25]= w3
                w2['p10'] = w3.quantile(q=0.1, axis = 1)
                w2['Median'] = w3.quantile(q=0.5, axis = 1)
                w2['p90'] = w3.quantile(q=0.9, axis = 1)
           w2.to_csv(outpath+mrcN+'_'+ind+'_'+r+'.csv', sep=',',index=True)
           
           
os.chdir(outpath)
for r in rcps:
    for m in mrcs:
        list = glob.glob('*'+m+'*'+r+'*.csv')
        writer = pd.ExcelWriter(output+m+'_'+r+".xlsx")
        for df in list:
            df2 = pd.read_csv(df)
            df2 = df2.rename(columns={'Unnamed: 0.1': 'Year'})
            df2.index = df2['Year']
            df2.drop(df2.columns[[0,1,]], axis=1, inplace=True)
            df2.to_excel(writer, sheet_name= df.split("_")[1]+'_'+df.split("_")[2])
        writer.save()
print('It took', (time.time() - start) / 60.0, 'minutes.')    

