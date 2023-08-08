

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import seaborn as sns

#################################################
""" This function will open specified netCDF files to create a probability density plot of values along with a box plot of the value range 
creating a violin plot as the end product to show multimodal distributions. """

input= 'R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/downscaling/point_data/'

#Change output file depending on time period comparison
outputViolin='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/Violin_Plot_Statistical_Downscaling_Methods_Tasmax_1981to2010_Test.png'

#Use these settings for 1981-2010 violin plot
list_nc = ['tasmax_anusplin_daily_1981to2010.nc', 'tasmax_CanESM2_daily_1981to2010_BCCAQ2.nc',
           'tasmax_CanESM2_daily_1981to2010_qm_Celsius_Nicolas.nc', 'tasmax_CanESM2_daily_1981to2010_biasCorrected.nc',
           'tasmax_CanESM2_daily_1981to2010_raw.nc']

list_names=['ANUSPLIN','BCCAQ2','QM', 'Mean Bias Corr.', 'RAW GCM']

palette = {'ANUSPLIN':'firebrick','BCCAQ2':'coral','QM':'seagreen', 'Mean Bias Corr.':'palegreen', 'RAW GCM':'orchid'}

# the list_name coresponds to the name that will be put on the OX ax. 
#They must be in the same order as the files in list_nc

# Put here the name of the netCDF variable
var='tasmax'
# Put here what to mention on the oy ax
oy_label='Tasmax [$^\circ$C]'
# Put here what to mention on the ox ax
ox_label='Method'

plot_title='Comparison of Statistical Downscaling Methods 1981-2010'
font_size=20

########################################################

ds=xr.open_dataset(input+list_nc[0])
DataF = pd.DataFrame({'values':(ds[var].values).flatten()})
DataF[ox_label] = [list_names[0]]*np.size(DataF)
median_obs=np.median((ds[var].values).flatten())

for fld,name in zip(list_nc[1:],list_names[1:]):
    print(fld,name)
    ds = xr.open_dataset(input+fld)
    data1 = pd.DataFrame({'values':(ds[var].values).flatten()})
    data1[ox_label] = [name]*np.size(data1)    
    DataF = DataF.append(data1)
 

#figure
sns.set_style("ticks")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2})

fig1 = plt.figure(figsize=(16,8))
#For 1981-2010
ax = sns.violinplot(x="Method", y="values", data=DataF, palette=palette)
#For 2071-2100
#ax = sns.violinplot(x="Method", y="values", data=DataF, palette=palette2)

#ax=sns.violinplot(DataF,scale="count", jitter=True, palette=palette, alpha=0.2, cut=0,  inner="stick",linewidth=1, orient='v')
#ax=sns.violinplot(DataF,scale="count", jitter=True, palette=palette, alpha=0.2, cut=0,  inner='box',orient='v')
ax.tick_params(labelsize=24)
plt.ylabel(oy_label, fontsize=28)
plt.axhline(y=0.0, linewidth=2, linestyle='--', color = 'k')
plt.axhline(y=median_obs, linewidth=2, linestyle='--', color = 'b')
plt.xticks(rotation=10, ha='right')
plt.title(plot_title, fontsize=font_size)
plt.tight_layout()
plt.savefig(outputViolin)
fig1.clf()








