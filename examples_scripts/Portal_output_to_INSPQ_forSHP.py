# -*- coding: utf-8 -*-
"""
This script converts the 30ymean_p50p10p90 csv output from Emilia's shapefile scripts into csv files for each period, percentile and RCP

"""


import time 
import pandas as pd
from pandas import ExcelWriter
import xarray
import glob, os
import numpy as np



input='P:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/08 - Projects & Tasks/01 - DPO/INSPQ/OutputQC/'
output='C:/Users/pomeroyc/Desktop/INSPQ/QC/forSHP/'

rcps = ['rcp45', 'rcp85']

percs = ['p10','p50','p90']

years = ['1981', '2011', '2041']

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
    for p in percs:
        for y in years:
            os.chdir(input+'tx_max'+'/'+r+'/YS/')
            w = pd.read_csv('tx_max'+'_'+mrcs[0]+'_'+r+'_'+'30y_Means_p50p10p90.csv')
            w.index = w.iloc[:,0]
            w2 = pd.DataFrame()
            #take SHP file columns
            #w2 = w.iloc[:,[0,4,5]]
            #remove extra year column
            #w2 = w2.iloc[:,[1,2]]
            #add regions as rows and indices as columns
            for m in mrcs:
                for ind in indices:
                    #change directory to index and rcp of interest
                    os.chdir(input+ind+'/'+r+'/YS/')
                    w = pd.read_csv(ind+'_'+m+'_'+r+'_'+'30y_Means_p50p10p90.csv')
                    w.index = w.iloc[:,0]
                    w2.loc[m,'RSS_code'] = w.loc[int(y), 'RSS_code']
                    w2.loc[m,ind+'_'+r+p] = w.loc[int(y),ind+'_'+r+p]
                    if ind == 'tn_min' or ind == 'tg_mean' or ind == 'tx_max' or ind == 'tx_mean' or ind == 'tn_mean':
                        w2.loc[m,ind+'_'+r+p] = w2.loc[m,ind+'_'+r+p] - 273.15
                    else:
                        w2 = w2
                    w2.index.name ='RSS_nom'
                    w2.to_csv(output+y+'_'+p+'_'+r+'.csv', sep=',',index=True)
                    
print('It took', (time.time() - start) / 60.0, 'minutes.')    

