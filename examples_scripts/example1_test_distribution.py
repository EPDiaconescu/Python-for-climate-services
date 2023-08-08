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

# This script will open an 1D netcdf files (ex. data at one grid point) and plot the distribution of values.
# The distribution is represented by an empirical PDF of values


# Put in input the path to the folder with your netCDF files
input='Y:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/downscaling/'

# Put here the name of the netcdf file
fld='tasmax_anusplin_daily_1981to2010.nc'

# Put in output the path to the folder where you want to save the figure with the name of the figure
output='C:/Users/DiaconescuE/Desktop/test/test_kde.png'

# Put here the name of the netCDF variable
var='tasmax'

font_size = 20
x_eval = np.linspace(-40, 40, num=40)
legend='Observations'
ylabel='empirical PDF'
xlabel='TASMAX'


#################################################

ds = xarray.open_dataset(input+fld)
data = (ds[var].values).flatten()
fig, ax = plt.subplots(figsize=(8,8))

kdeA = kde(data, x_eval, bandwidth=4)
ax.plot(x_eval, kdeA, 'b-',linewidth=2, label=legend)

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

