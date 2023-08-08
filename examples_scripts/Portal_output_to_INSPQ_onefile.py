# -*- coding: utf-8 -*-
"""
This script converts the 30ymean_p50p10p90 csv output from Emilia's shapefile scripts into excel documents for each region 
Each document has a sheet for each index
"""


import time 
import pandas as pd
from pandas import ExcelWriter
import xarray
import glob, os
import numpy as np



input='P:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/08 - Projects & Tasks/01 - DPO/INSPQ/OutputMRS/'
outpath='C:/Users/pomeroyc/Desktop/INSPQ/MRC/outpath/'
outpath2='C:/Users/pomeroyc/Desktop/INSPQ/MRC/outpath2/'
output='C:/Users/pomeroyc/Desktop/INSPQ/MRC/output/'

rcps = ['rcp45', 'rcp85']

indices= ['tx_max', 'tn_min', 'tg_mean', 'tn_mean', 'frost_days', 'ice_days',
          'tx_mean', 'tnlt_-15', 'tnlt_-25', 'txgt_25', 'txgt_30', 'txgt_32',
          'gddgrow_5', 'gddgrow_10', 'gddgrow_0', 'rx1day', 'r1mm', 'r10mm',
          'prcptot', 'tr_18', 'tr_20', 'cddcold_18', 'hddheat_17']

start = time.time()

#name of regions
mrcs = []
os.chdir(input+'tx_max'+'/'+'rcp45'+'/YS/')
list=glob.glob('tx_max'+'*30y_Means_allModels*.csv')
for g in list:
    mrcN=g.split("_")[-5]
    mrcs.append(mrcN)


for r in rcps:
    for ind in indices:
        #change directory to index and rcp of interest
        os.chdir(input+ind+'/'+r+'/YS/')
        #list all 30ymeans
        list=glob.glob(ind+'*30y_Means_p50p10p90*.csv')
        for g in list:
           #open file
           w = pd.read_csv(g)
           #name of region
           mrcN=g.split("_")[-5]
           #extract 3 time periods of interest
           w2 = w.iloc[[3,6,9],]
           #add percentiles at the end + ensure that data is in the right units
           if ind == 'tn_min' or ind == 'tg_mean' or ind == 'tx_max' or ind == 'tx_mean' or ind == 'tn_mean':
                w2.iloc[:,[1,2,3]] = w2.iloc[:,[1,2,3]] - 273.15
           else:
                w2 = w2      
           w2.to_csv(outpath+mrcN+'_'+ind+'_'+r+'.csv', sep=',',index=True)
           
           
os.chdir(outpath)
for m in mrcs:
    for ind in indices:
        list = glob.glob('*'+m+'*'+ind+'*.csv')
        cs1 = pd.read_csv(list[0])
        cs2 = pd.read_csv(list[1])
        cs3 = cs1.iloc[:,1:5].join(cs2.iloc[:,2:8])
        cs3.to_csv(outpath2+m+'_'+ind+'.csv', sep=',',index=True)

        


os.chdir(outpath2)
for m in mrcs:
    list = glob.glob('*'+m+'*.csv')
    writer = pd.ExcelWriter(output+m+".xlsx")
    for df in list:
        df2 = pd.read_csv(df)
        df2 = df2.rename(columns={'Unnamed: 0.1': 'Year'})
        df2.index = df2['Year']
        df2.drop(df2.columns[[0,1,]], axis=1, inplace=True)
        df = df.split(".")[0]
        df2.to_excel(writer, sheet_name= df.split("_", 1)[1])
    writer.save()
print('It took', (time.time() - start) / 60.0, 'minutes.')    

