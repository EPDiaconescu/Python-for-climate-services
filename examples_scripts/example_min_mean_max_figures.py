
import xarray
import matplotlib.pyplot as plt

def min_mean_max_figures(file, var, attributes='YES',x='lon', y='lat', cmap='BrBG_r', levels=22):
    """ The function will plot three figures showing the minimum, maximum and the mean values over the entire period
	files = put here the path and the name of the netCDF file
	var=put here the name of the variable you want to plot (ex. 'tas')
	attributes = put 'YES' if you want to see the attributes of the variable
	x= put the name of the dimension ox
	y= put the name of the dimension 0y
	cmap= put the name of the color scale to use
	levels= put the number of colors to use.
    """
    ds = xarray.open_dataset(file, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    if attributes=='YES':
        print(ds[var].attrs)
        print('  ')
    fig1 = plt.figure()
    ds[var].min(dim='time').plot.contourf(x=x, y=y, cmap=cmap, levels=levels);
    plt.title('Minimum')

    fig2 = plt.figure()
    ds[var].mean(dim='time').plot.contourf(x=x, y=y, cmap=cmap, levels=levels);
    plt.title('Mean')

    fig3 = plt.figure()
    ds[var].max(dim='time').plot.contourf(x=x, y=y, cmap=cmap, levels=levels);
    plt.title('Maximum')
    plt.show()

    return

################ EXAMPLE ###################

# Put in input the path and the netCDF file you want to analyze
input= 'G:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
fld='tas_hist_canesm2_mm.nc'
var='tas'
min_mean_max_figures(input+fld,'tas', attributes='YES',x='lon', y='lat', cmap='BrBG_r', levels=22)
