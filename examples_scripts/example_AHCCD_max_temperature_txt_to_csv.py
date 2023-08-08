# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:03:28 2019

@author: chowk

Script to Read and Save AHCCD text files
"""
#%% Packages/modules
import os
import time
import pandas as pd
import csv
import re
import xarray as xr
import numpy as np
start = time.time()
#%% Inputs

input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/Climate Data Requests Input Data/AHCCD Practice Data/'
#output='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/Climate Data Requests Output Data/'
os.chdir(input)

filelist = os.listdir(input)

#%% Converting text file into semi-structured .csv file

#for x in range(0,len(filelist)):
    #Reads text file as a list
    with open(input+filelist[0], 'r') as file:
        test = file.readlines()
        file.close()

    indices = 1,3 #These are the index numbers of the French headings to be removed
    test = [y for z, y in enumerate(test) if z not in indices] #Removes headings from list
    test = [v.replace('-9999.9M', '  -9999.9M') for v in test] #Adds a space to the missing value indicator for delimiting
    test = [v.replace('-9999.9m', '  -9999.9M') for v in test]
    test = [v.replace('Day ', '') for v in test] #Removes 'Day ' for easier parsing 

    #Following are the space strings within the headers and data that are to be reduced
    headerGap = '          '
    dataGap= '     '
    
    #Goes through the list to remove as many blank spaces as possible, then replaces the gaps with a comma for delimiting
    for j in range (0,len(test)): 
        if j == 0:
            for i in range(len(headerGap), 0, -1):
                test[j] = re.sub (headerGap[0:i],headerGap[0:i-1],test[j])
            test[j] = re.sub (headerGap[0:2],',',test[j])   
        elif j >= 1:
            test[j] = test[j][1:test[j].find(' ',1)]+' '+test[j][test[j].find(' ',1):len(test[j])]
            if j == 1:
                test[j] = re.sub ('  ',',',test[j])
            else:
                for k in range(len(dataGap), 1, -1):
                    test[j] = re.sub (dataGap[0:k],dataGap[0:k-1],test[j])
                test[j] = re.sub (dataGap[0],',',test[j])
        test[j] = re.sub ('\n','',test[j])
    
    #Writes as a .csv file to be reread for further processing
    with open(output+'tempfile.csv', 'w') as myfile:
        wr = csv.writer(myfile, delimiter='\n', quoting=csv.QUOTE_NONE,escapechar = ' ')
        wr.writerow(test)
        myfile.close()

    hframe = pd.read_csv(output+'tempfile.csv', header = None, nrows = 1) #Makes a dataframe that just includes metadata description headings
                                                                      #df can't be properly constructed if these are included with the data since the headings
                                                                      #are of different dimensions
    dframe = pd.read_csv(output+'tempfile.csv', header = 1, usecols = range (0,33)).reset_index().drop(columns = ['index'])#Makes a separate heading of just the data
    date = pd.concat([dframe.pop('Year'),dframe.pop('Mo')], axis = 1)#Pops out the columns of Years and Months as separate df
    date = date.iloc[np.repeat(np.arange(len(date)),len(dframe.iloc[0,:]))].reset_index().drop(columns = ['index'])#
    frame = dframe.T

    days = pd.DataFrame({'Day':range(1,32)})
    days = days.iloc[np.tile(np.arange(len(days)),len(dframe.iloc[:,0]))].reset_index().drop(columns = ['index'])

    dframe = dframe.stack().reset_index().drop(columns = ['level_0','level_1']).astype(str)
  
    result = pd.concat([date,days,dframe], axis =1, ignore_index = True)
    result = result.rename(columns={0:"Year", 1:"Month", 2:"Day", 3:"MaxTemp"})
    
    result['Qualifier'] = result.MaxTemp.apply(lambda y: y[-1] if y[-1] == 'M' or y[-1] == 'E' or y[-1] == 'a' else '')
    result.MaxTemp = result.MaxTemp.apply(lambda z: z[0:-1] if z[-1] == 'E' or z[-1] == 'a' else z)
    result.MaxTemp = pd.to_numeric(result.MaxTemp, errors = 'coerce')
    result['Date'] = pd.to_datetime((result.iloc[:,0:3]), errors = 'coerce')
    result = result.dropna(subset = ['Date'])
    cols = result.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    result = result[cols]

    result.to_csv(output + str(hframe[4][0])+'_'+ str(hframe[1][0])+'_'+str(result.Year.iloc[0])+'to'+str(result.Year.iloc[-1])+'.csv')
    os.remove(output+'tempfile.csv')

print('It took', time.time()-start, 'seconds.')


#%%