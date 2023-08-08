# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:51:53 2019

@author: DiaconescuE
"""

#The empirical distribution function estimates the underlying CDF of the points in the sample. 
#We estimate the CDF (cumulative distribution function) after classifying data into some bins. 
#This means, we assumed that the data behaves in a statistical similar way over some small range. 
#We can estimate the CDF without making this assumption also, which would be done using ECDF function (the empirical CDF). 
#The output form ECDF function is a object which store the value of data and their corresponding ECDF. 
#The data is retrieved using ecdf.x and their corresponding ECDF is retrieved using ecdf.y. 

import xarray
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gaussian_kde
import statsmodels.api as sm


# This script will open two 1D netcdf files (ex. data at one grid point) and plot the distribution of values on the same graphic.
# The distribution is represented by an empirical PDF of values


# Put in input the path to the folder with your netCDF files
input='R:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/downscaling/point_data/'

# Put here the name of the 2 netcdf file
fld1='pr_anusplin_daily_1981to2010.nc'
fld2='pr_CanESM2_daily_2071to2100_raw.nc'

# Put in output the path to the folder where you want to save the figure with the name of the figure
output='M:/Python training files/'

# Put here the name of the netCDF variable
var='pr'

font_size = 24
x_ticks = np.array([0.,10., 20., 30., 40., 50., 60., 70., 80., 90., 100.])
y_ticks = np.array([0.,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.])
legend1='Observations'
legend2='GCM - raw data'
ylabel='empirical CDF'
xlabel='PR'


#################################################
# open first data
ds1 = xarray.open_dataset(input+fld1)
data1 = (ds1[var].values).flatten()

# open second data
ds2 = xarray.open_dataset(input+fld2)
data2 = (ds2[var].values).flatten()

ecdf1 = sm.distributions.ECDF(data1)
ecdf2 = sm.distributions.ECDF(data2)

fig, ax = plt.subplots(figsize=(12,8))

ax.plot( ecdf1.x, ecdf1.y, linewidth = 3, color='blue',label=legend1)
ax.plot( ecdf2.x, ecdf2.y, linewidth = 3, color='red', label=legend2)

plt.xticks(x_ticks,fontsize=font_size)
plt.xlabel(xlabel, fontsize=font_size)
plt.ylabel(ylabel, fontsize=font_size)
plt.yticks(y_ticks,fontsize=font_size)


ax.axvline(x=0.0, linewidth=2, ls='--', color='k')

lg=plt.legend(loc=4, fontsize=18)
lg.draw_frame(False)


plt.tight_layout()
plt.savefig(output)
plt.plot()

