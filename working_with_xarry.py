#xarray and working with netCDF files

import xarray
import matplotlib.pyplot as plt
import glob, os
import numpy as np
import pandas as pd
import nc_time_axis
import cftime

# Each python script begin with importing the modules you will nead. 
# xarray: Python module specially construct to work with multi-dimensional data.
# Matplotlib: Python module useful for plotting
# Glob and os are modules that permits to work with file system
# Numpy : Python module that permits to work with array
# Pandas: Python module that permits to work with tables (named data frame)
# to instal nc-time-axis us ein Anaconda Prompt : conda install -c conda-forge nc-time-axis

# GCM and RCM outputs are multi-dimensional data often provided in NetCDF format. 
# We will use xarray to open and manipulate netCDF files
##########################################3

# 1)	Working with only one file
# First we indicate the folder where the data is and the file that we want to open (pay attention to /):
input= 'F:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
fld='x_test_cdo.nc'

# Please, verify the two parameters by typing:
input
fld
input+fld

#to open the netCDF fil, we will use the function open_dataset from the xarray module, 
#indicating in the brackets the path to the file and the file we want to open. Please do:
ds = xarray.open_dataset(input+fld, decode_times=False)
ds['time'] =  xarray.decode_cf(ds).time

# xarray.Dataset is an in-memory representation of a netCDF file. You have created a link to your data that is named ds. 
# By simply typing ds, you will obtain information about this data. Please do:
ds
# How many dimensions your data have? How many coordinates? How many variables are in the files? 
# What are the name of the dimensions and how long they are?
# To see just the dimensions of the file do:
ds.dims

#To see the coordinated do:
ds.coords

#Dimensions provide names that xarray uses instead of the axis argument found in many numpy functions. 
# Coordinates enable fast label based indexing and alignment, building on the functionality of the index found on a pandas DataFrame or Series.
#To see the attributes associated with the file do:
ds.attrs

#To see the name of variables in the file do:
ds.data_vars

# To registration the variables into a list named l, do:
l=[]
for v in ds.data_vars:
	l.append(v)

#To see the attributes to one variable (here tasmax):
ds.tasmax.attrs

#To extract the values of different coordinates or variables:
#-	The longitudes: ds['lon'] or just the values into an array that we will name lon_array (lon_array=ds['lon'].values); to see the array: lon_array
ds['lon']
lon_array=ds['lon'].values
lon_array

#-	The latitudes: ds['lat'] or just the values into an array that we will name lat_array (lat_array=ds['lat'].values); to see the array: lat_array
ds['lat']
lat_array=ds['lat'].values
lat_array

#-	The time: ds['time'] or ds['time'].values for an array 
ds['time'] 
ds['time'].values

#-	If you want just the years for each timestep and want to transform the array into a pandas series or pandas data frame
yy0= ds['time.year'].values
yy1=ds['time.year'].to_series() 
yy2= ds['time.year'].to_dataframe()

#try also: 
ds['time.month'].values 
ds['time.day'].values


#-	The values for tasmax:  tasmax_ds=ds['tasmax'] and tasmax_array=ds['tasmax'].values 
#(the diference between the two is that the first one is a xarray with dimensions named as in the previous ds file, 
#while the second is now a numpy array with dimensions noted 0, 1 and 2.) 
# it is indicated to work with an xarray and not with a numpy array if you want to same later the result in netCDF.
tasmax_ds=ds['tasmax']
tasmax_array=ds['tasmax'].values 

#We can do arithmetical operations directly on the selected variable:
New_tasmax=tasmax_ds-15.0

#Verify the new data:
New_tasmax

#To add global attributes to the new netCDf file that contain an history of what you have done 
# and also information about the original file by copying general attributes from the original file:
New_tasmax.attrs['history'] = 'tasmax-15.0'

#Look again to the file:
New_tasmax

#To copy attributes from the initial file (ds) to the new one:
#New_tasmax.attrs[' downscaling_method_id ']=ds. attrs[' downscaling_method_id ']

#Look again to the file:
New_tasmax

#To save in netCDF the new data (the new file will have the name exactly the same with the first but with the last 3 characters (.nc) replaces by new.nc)
fileout=fld[:-3]+'_new.nc'
New_tasmax.to_netcdf(input+fileout)

#Please, verify the new saved netCDF file using panoply

#We can apply operations over dimensions by name: 
Tasmax_sum=tasmax_ds.sum('time')
Tasmax_mean=tasmax_ds.mean('time')
Tasmax_min=tasmax_ds.min('time')
Tasmax_mean=tasmax_ds.max('time')

#The results of those operations are two-dimensional files: latitude and longitude. 
#To have a quick plot for the two dimensional file use:
Tasmax_mean.plot()

# Example operation on latitude and longitude:
Tasmax_spatialmean= tasmax_ds.mean(['lat','lon'])

#Tasmax_spatialmean is the result of two operations, one over the latitudes and one over the longitudes. 
# The result is a one dimensional file with the dimension time. To have a quick plot of this time evolution use 
Tasmax_spatialmean.plot()


#We can select values by label, for example select the field for the date 2053-03-06
T1=tasmax_ds.sel(time='1950-01-02')

#This is again a two dimensional filed (dimensions: longitude and latitude) and we can plot it quickly with: 
T1.plot()



#Suppose we have a 3D file covering Canada with the time as monthly means for several years. 
File_mm= 'F:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/pr_rcp26_cnrmcm5_monthlyMean.nc'
#We open the file using xarray: 
ds = xarray.open_dataset(File_mm, decode_times=False)
ds['time'] = xarray.decode_cf(ds).time

#You can select all January months for all years using:
data_01 =ds.sel(time=ds['time.month']==1)
#To select just the February months:
data_02 =ds.sel(time=ds['time.month']==2)
#You can save the file in netCDf and visualize with Panoply.
data_02.to_netcdf('F:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/test_februart.nc')

#Other operations:
#-	To compute annual mean for a dataset with monthly or daily data use:
new_data=ds.resample(time='AS').mean('time')
#-	To compute monthly means for a dataset with daily data use:
new_data=ds.resample(time='MS').mean('time')
#-	To compute seasonal means, with the winter season starting on December 1st, use:
new_data=ds.resample(time="QS-DEC").mean('time')



#Try also to select a grid point with values situated in the data file:
T2=tasmax_ds.sel(lat=45.12, lon=-76.21, method='nearest')

#And plot the time series: 
T2.plot()

#Try select a period: 
T3=tasmax_ds.sel(time=slice('1950-02-01', '1950-03-01'))

#2)	Working with several files situate din one folder:
# Put in input the path to the netCDF file you want to analyze and in output the folder where you want to save the new files
input= 'F:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
output= 'F:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'

#First we go in the directory indicated in input:
os.chdir(input)

#We construct a list containing all the file in this directory that begin with tas and are ended with .nc
List1=glob.glob('tas*.nc')

#Try to see the list:
List1

#We construct a loop, which will call the function for each files we put in the list
for fld in list[:]:   
	print(fld)
	#……………………………..
	#fileout = fld[:-3] + '_test_new.nc'


