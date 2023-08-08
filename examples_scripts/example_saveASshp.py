# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 09:29:51 2020

@author: DiaconescuE
"""

import time
import pandas as pd
import geopandas as gpd
import os

start = time.time()
period='1981'
percentile='p10'
rcp='rcp45'

input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/example_SaveAsSHP/'
input_shp='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/example_SaveAsSHP/GIS-QC_Test/'
output_shp='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/example_SaveAsSHP_output/'
fp=input_shp+'QC.geojson'
new_name_shp="test_output_"+period+"_"+percentile+"_"+rcp+"_QC.shp"

name_col_code='RSS_code'

##########################################

w = pd.read_csv(input+ 'ex_QC_'+period+'_'+percentile+'_'+rcp+'.csv')
#del w['RES_NM_REG']


list_ind0=w.columns.tolist()[2:]
w.columns=w.columns[:2].tolist()+[name[:-9] for name in list_ind0]
list_ind=w.columns.tolist()[2:]


output_fp = os.path.join(output_shp, new_name_shp)

data = gpd.read_file(fp)
#data.plot();
#data.columns

#data[name_col_code]

# define a new column for area
for ind in list_ind:
    print(ind)
    data[ind] = None
    # iterate and calculate
    for index, row in data.iterrows():
        print(index, row[name_col_code], w[w[name_col_code]==int(row[name_col_code])][ind].tolist())
        data.loc[index, ind] = w[w[name_col_code]==int(row[name_col_code])][ind].tolist()[0]
    

data.to_file(output_fp)

print('It took', time.time()-start, 'seconds for '+ period +'_'+ percentile + '_' + rcp)
 