from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib  as mpl
import glob, os
import time



def summary_stats(input,fld,varName,TimeI):
    """ ???
    """
   
    nc = Dataset(input + fld)
    lats0 = nc.variables['lat'][:]
    lons0 = nc.variables['lon'][:]
    lons0, lats0 = np.meshgrid(lons0, lats0)
    data0 = nc.variables[varName][TimeI,:,:]
    
    data_1d = data0.flatten()
    
    return stats.describe(data_1d)
    
    
    
    

   

################ EXAMPLE 1 ################################
#we start a chronometer
start = time.time()
# we indicate the folder were the 2D netCDF fie is
input= 'N:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/09 - Portal/Subset of Portal Data/BCCAQ/'
# we indicate the folder were the figure will be saved
output = 'N:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'
# we indicate the name of the variable we want to plot
varName='ice_days_p50'

# we put here the name of the 2D netCDF file
fld='BCCAQv2+ANUSPLIN300_ensemble-percentiles_historical+rcp26_1950-2100_ice_days_YS.nc'
# we put here the name of the figure to save in output folder
# here I choose to use the same name as the initial file and to replace the last 3 characters of the name with _Canada.png
imgout=fld[:-3]+'_Canada.png'

# we apply the function with the standard options
summary_stats(input, fld, varName, 0)
# we print the number of seconds it took to run the script
print('It took', time.time()-start, 'seconds.')


# ############## EXAMPLE 2 ################################
# # the following script will plot all the files that are in the directory indicated in input
# # and save the figures in the directory indicated in output using the same name for figures as the netCDF file

# input= 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/eccc_data/CMIP5_processed/wind_speed/'
# output = 'H:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'
# varName='sfcWind'
# # first we go in the directory indicated in input
# os.chdir(input)ee
# # we construct now a list containing all the file in this directory that are ended with .nc
# list=glob.glob('sfcWind_Amon_ens_rcp85*pctl50.nc')
# # we construct a loop, which will call the function Arctic_figure for each files we put in the list

# for fld in list[:]:
    # print(fld)
    # imgout=fld[:-3]+'.png'
    # clevs = np.array([-66, -60., -54., -48., -42., -36., -30., -24., -18.,-12., -6., -2.,
                   # 2., 6., 12., 18., 24., 30., 36., 42., 48., 54., 60.])
    # Canada_figure(input, fld, varName, fld, output,imgout)
    

