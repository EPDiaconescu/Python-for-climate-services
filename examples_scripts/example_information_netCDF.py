import xarray
import sys

def information_netCDF(files,time='YES',lat='YES',lon='YES',output='Screen'):
    """This function prints the short name of variables and their dimensions
	The dimensions of the field must be noted with time, lon and lat to obtain the information about them
	files = put here the path and the name of the netCDF file
	time = put 'YES' if you want information about the time dimension or anything else if not
	lat = put 'YES' if you want information about the lat dimension or anything else if not
	lon = put 'YES' if you want information about the lon dimension or anything else if not
	output = put 'Screen' idf you want the information printed on the screen or
    the path and the txt file if you want the information to be written into a txt file   """
    ds = xarray.open_dataset(files, decode_times=False)
    ds['time'] = xarray.decode_cf(ds).time
    if output=='Screen':
        print(ds.data_vars)
        print('  ')
        print('The dimensions are : ')
        print(ds.dims)
        if time=='YES':
            if ds.time.size > 1:
                print('There are ' + str(ds.time.values.size) + ' time steps')
                print('The first time step is : ' + str(ds.time.values[0]))
                print('The second time step is : ' + str(ds.time.values[1]))
                print('The last time step is : ' + str(ds.time.values[-1]))
            else:
                print('There is only ' + str(ds.time.values.size) + ' time step')
                print('The first time step is : ' + str(ds.time.values[0]))
            print('  ')
        if lat=='YES':
            if ds.lat.size > 1:
                print('There are ' + str(ds.lat.values.shape) + ' grid points for latitudes')
                if ds.lat.values[0].size==1:
                    print('The first latitude is : ' + str(ds.lat.values[0]))
                    print('The second latitude is : ' + str(ds.lat.values[1]))
                    print('The last latitude is : ' + str(ds.lat.values[-1]))
                else:
                    print ('The smallest latitude is : '+ str(ds.lat.values.min()))
                    print ('The greatest latitude is : ' + str(ds.lat.values.max()))
            else:
                print('There is only ' + str(ds.lat.values.size) + ' latitude grid point')
                print('The latitude is : ' + str(ds.lat.values[0]))
            print('  ')
        if lon=='YES':
            if ds.lon.size > 1:
                print('There are ' + str(ds.lon.values.shape) + ' grid points for longitude')
                if ds.lon.values[0].size==1:
                    print('The first longitude is : ' + str(ds.lon.values[0]))
                    print('The second longitude is : ' + str(ds.lon.values[1]))
                    print('The last longitude is : ' + str(ds.lon.values[-1]))
                else:
                    print ('The smallest longitude is : '+ str(ds.lon.values.min()))
                    print ('The greatest longitude is : ' + str(ds.lon.values.max()))
            else:
                print('There is only ' + str(ds.lon.values.size) + ' longitude grid point')
                print('The longitude is : ' + str(ds.lon.values[0]))
            print('  ')
    else:
        orig_stdout = sys.stdout
        outF = open(output, "w")
        sys.stdout = outF
        print(ds.data_vars)
        print('  ')
        if time=='YES':
            if ds.time.size > 1:
                print('There are ' + str(ds.time.values.size) + ' time steps')
                print('The first time step is : ' + str(ds.time.values[0]))
                print('The second time step is : ' + str(ds.time.values[1]))
                print('The last time step is : ' + str(ds.time.values[-1]))
            else:
                print('There is only ' + str(ds.time.values.size) + ' time step')
                print('The first time step is : ' + str(ds.time.values[0]))
            print('  ')
        if lat=='YES':
            if ds.lat.size > 1:
                print('There are ' + str(ds.lat.values.shape) + ' grid points for latitudes')
                if ds.lat.values[0].size==1:
                    print('The first latitude is : ' + str(ds.lat.values[0]))
                    print('The second latitude is : ' + str(ds.lat.values[1]))
                    print('The last latitude is : ' + str(ds.lat.values[-1]))
                else:
                    print ('The smallest latitude is : '+ str(ds.lat.values.min()))
                    print ('The greatest latitude is : ' + str(ds.lat.values.max()))
            else:
                print('There is only ' + str(ds.lat.values.size) + ' latitude grid point')
                print('The latitude is : ' + str(ds.lat.values[0]))
            print('  ')
        if lon=='YES':
            if ds.lon.size > 1:
                print('There are ' + str(ds.lon.values.shape) + ' grid points for longitude')
                if ds.lon.values[0].size==1:
                    print('The first longitude is : ' + str(ds.lon.values[0]))
                    print('The second longitude is : ' + str(ds.lon.values[1]))
                    print('The last longitude is : ' + str(ds.lon.values[-1]))
                else:
                    print ('The smallest longitude is : '+ str(ds.lon.values.min()))
                    print ('The greatest longitude is : ' + str(ds.lon.values.max()))
            else:
                print('There is only ' + str(ds.lon.values.size) + ' longitude grid point')
                print('The longitude is : ' + str(ds.lon.values[0]))
            print('  ')

        sys.stdout = orig_stdout
        outF.close()
    return


################ EXAMPLE ###################

# Put in input the path to the netCDF file you want
input= 'W:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingData/'
# Put here the name of the netCDF file to want
fld='tas_hist_gisse2h.nc'
# Put in output the path to the folder where you want to save the information if you want to put the information into a txt file
out_folder='W:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/02 - Code/python/trainingOutput/'
# Put here the name of the txt file you want to create
txt_file='test1.txt'

# to se only which variables are and what are their dimensions:
information_netCDF(input+fld,time=' ',lat=' ',lon=' ',output='Screen')

# for all information in output
information_netCDF(input+fld,time='YES',lat='YES',lon='YES',output=out_folder+txt_file)
