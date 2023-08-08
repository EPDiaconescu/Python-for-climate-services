# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:51:53 2019

@author: DiaconescuE
"""

import xarray
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gaussian_kde

def kde(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scipy"""
    kde = gaussian_kde(x, bw_method=bandwidth / x.std(ddof=1), **kwargs)
    return kde.evaluate(x_grid)

# This script will open two 1D netcdf files (ex. data at one grid point) and plot the distribution of values on the same graphic.
# The distribution is represented by an empirical PDF of values


# Put in input the path to the folder with your netCDF files
input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/downscaling/'

# Put here the name of the 2 netcdf file
fld1='tasmax_anusplin_daily_1981to2010.nc'
fld2='tasmax_CanESM2_daily_2071to2100_raw.nc'

# Put in output the path to the folder where you want to save the figure with the name of the figure
output='C:/Users/DiaconescuE/Desktop/test/test_kde2.png'

# Put here the name of the netCDF variable
var='tasmax'

font_size = 20
x_eval = np.linspace(-60, 60, num=60)
legend1='Observations'
legend2='GCM - raw data'
ylabel='empirical PDF'
xlabel='TASMAX'


#################################################
# open first data
ds1 = xarray.open_dataset(input+fld1)
data1 = (ds1[var].values).flatten()

# open second data
ds2 = xarray.open_dataset(input+fld2)
data2 = (ds2[var].values).flatten()


fig, ax = plt.subplots(figsize=(8,8))

# compute and plot the first PDF
kdeA = kde(data1, x_eval, bandwidth=4)
ax.plot(x_eval, kdeA, 'b-',linewidth=2, label=legend1)


# compute and plot the second PDF
kdeB = kde(data2, x_eval, bandwidth=4)
ax.plot(x_eval, kdeB, 'r-',linewidth=2, label=legend2)


ax.axvline(x=0.0, linewidth=2, ls='--', color='k')

plt.legend(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.xticks(fontsize=font_size)
ax.set_ylabel(ylabel,fontsize=font_size)
ax.set_xlabel(xlabel,fontsize=font_size)
ax.set_xlim(np.min(x_eval)-10,np.max(x_eval)+10)
ax.set_ylim(np.min(kdeA),np.max(kdeA)+(np.max(kdeA)-np.min(kdeA))/6)

plt.tight_layout()
plt.savefig(output)
plt.plot()

