"""
This script allows the user to extract the spatial mean of all elements of any shapefile
This script does NOT use the THREDDS server and therefore downloads a bunch of files to do the computations on.
Sometimes urllib is finicky and will crash :(
The script will delete the downloaded files once it is done.
This can be done for annual data or 30y averages
A specific time period can be selected
The output is in CSV
To extract all grids within a shapefile, see the files marked "extract grids"

***Please make a copy of this script before editing***
"""

#%% run this before continuing
import threddsclient
from shapely.geometry import Point
import xarray as xr
import geopandas as gpd
from geopandas.tools import sjoin
import numpy as np
import pandas as pd
import time
import glob, os
import urllib
import salem

# Shapefile location and what you want to call the mask you create e.g. Provinces, health_regions etc.
inshp = r'P:/30. CLIMATE SERVICES DATA PRODUCTS OFFICE/03 - Data, Code & Models/01 - Data/Shapefiles/Provinces/gpr_000b11a_e.shp'
nameMask = 'Canada'
shdf = salem.read_shapefile(inshp)


#%%

# Where the CanadaWide netCDF files will be put
outpath = 'C:/Users/pomeroyc/Desktop/test_shapes/outpath/rcp26/'

# Where you want the final CSVs
output = 'C:/Users/pomeroyc/Desktop/test_shapes/Canada/'

# If mask netcdf file already created set to False.
# To create on the fly set to True to create the first time the through.
create_mask_flag = False

#%%This section requires the user to examine the shapefile to 
#  provide the name of the column that the region names appear in
col_name = 'PRENAME'

#%% Customize your output
# Indexes
indices = ['prcptot']

# RCPS
rcps = ['rcp26']


#%%

"""
#################################################################################################
#####################################Don't edit anything below!!##########################################
##################################################################################################
"""

#%% Don't edit this

def create_mask_from_shape(ds, poly):
    ds = ds.drop(ds.data_vars)
    ds = ds.drop('time')
    if len(ds.lon.shape) == 1 & len(ds.lat.shape) == 1:
        # create a 2d grid of lon, lat values
        lon1, lat1 = np.meshgrid(np.asarray(ds.lon.values), np.asarray(ds.lat.values))
    else:
        lon1 = ds.lon.values
        lat1 = ds.lat.values

    # create pandas dataframe from netcdf lat lon points
    df = pd.DataFrame(
        {'id': np.arange(0, lon1.size),
         'lon': lon1.flatten(),
         'lat': lat1.flatten()
         }
    )
    df['Coordinates'] = list(zip(df.lon, df.lat))
    df['Coordinates'] = df['Coordinates'].apply(Point)
    # create geodataframe (spatially refernced)
    gdf_pts = gpd.GeoDataFrame(df, geometry='Coordinates')
    gdf_pts.crs = {'init': 'epsg:4326'}

    # spatial join geodata points with region polygons
    pointInPoly = sjoin(gdf_pts, poly, how='left', op='within')
    # extract polygon ids for points
    mask = pointInPoly['index_right']

    mask_2d = np.array(mask).reshape(lat1.shape[0], lat1.shape[1])
    mask_2d = xr.DataArray(mask_2d, coords=ds.coords, dims=ds.dims)
    return mask_2d

# loop through indices and rcps
for ind in indices:

    for rcp in rcps:

        #for n in glob.glob(os.path.join(outpath, '*.nc')):
            #os.remove(n)
        
        ######################################################################
        start = time.time()
        
        url = 'https://pavics.ouranos.ca/thredds/catalog/birdhouse/cccs_portal/indices/Final/BCCAQv2/' + ind + '/YS/' + rcp + '/simulations/catalog.html'
        mods = sorted(['BNU-ESM', 'CCSM4', 'CESM1-CAM5', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'CanESM2', 'FGOALS-g2', 'GFDL-CM3',
                'GFDL-ESM2G', 'GFDL-ESM2M', 'HadGEM2-AO',
                'HadGEM2-ES', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM-CHEM', 'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR',
                'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M'
            , 'NorESM1-ME', 'bcc-csm1-1-m', 'bcc-csm1-1'])
        
        if not glob.os.path.exists(outpath):
            glob.os.makedirs(outpath)

        list_fld = []
        for m in mods:
            ncfiles = [ds for ds in threddsclient.crawl(url, depth=10) if m + '_' in ds.name]
            for n in ncfiles:
                if 'r1i1p1' in n.name:
                    list_fld.append(n)
                   
        # we start the download of files
        
        for l in list_fld:
            outfile = glob.os.path.join(outpath, l.name)
            urllib.request.urlretrieve(l.access_url(), outfile)

        print('Download finished')
        
        os.chdir(outpath)
        strng='*.nc'
        list_nc = glob.glob(strng)

        ds = xr.open_dataset(list_nc[0], decode_times=False)
        ds['time'] = xr.decode_cf(ds).time

        # create geopandas polygon
        poly = gpd.GeoDataFrame.from_file(inshp)

        reg_name = {k: i for i, k in enumerate(poly['PRENAME'])}
        if create_mask_flag:

            mask_2d = create_mask_from_shape(ds, poly)
            mask_2d.to_netcdf(os.path.join(os.path.dirname(inshp), 'mask_' + nameMask + '.nc'))
            with open(os.path.join(output, 'mask_' + nameMask + '_codeColors.cvs'), 'w', encoding="utf-8") as f:
                for key in reg_name.keys():
                    f.write("%s,%s\n" % (key, reg_name[key]))
            create_mask_flag = False
        else:
            mask_2d = xr.open_dataset(os.path.join(os.path.dirname(inshp), 'mask_' + nameMask + '.nc'))
            v = list(mask_2d.data_vars)[0]
            mask_2d = mask_2d[v]
        ds_means = {}
        for k in reg_name.keys():
            ds_means[k] = []

        # pd.DataFrame([reg_name]).to_csv()
        # mask_2d.plot()
        for model, nameM in zip(list_nc, mods):
            print(nameM)
            ds_m = xr.open_dataset(model, decode_times=False)
            ds_m['time'] = xr.decode_cf(ds_m).time
            ds_m = ds_m.where(ds_m.time.dt.year >= 1950, drop=True)
            ds_m = ds_m.where(ds_m.time.dt.month == 1, drop=True)
            ds_m = ds_m.load()
            # loop though regions
            for k in reg_name.keys():

                data_reg = ds_m.where((mask_2d == reg_name[k]), drop=True)
                ds_means0 = data_reg.mean(dim=['lon', 'lat']).to_dataframe()
                ds_means0.columns = [nameM + '_' + rcp]
                ds_means0.index = data_reg['time.year'].values 
                if not isinstance(ds_means[k], pd.DataFrame):
                    ds_means[k] = ds_means0
                else:
                    ds_means[k] = pd.concat([ds_means[k], ds_means0], axis=1)

        # export to csv # make a separate directory for each index
        out_ind = os.path.join(output, ind, rcp)
        if not os.path.exists(out_ind):
            os.makedirs(out_ind)
        for k in reg_name.keys():
            outfile = os.path.join(out_ind, ind + '_' + k.replace('/', '_') + '_' + rcp + '_AllYears_allModels.csv')
            id = poly[poly[col_name] == k]['PRUID'].values
            if len(id) > 1:
                raise Exception('to many ids')
            if ind == 'tn_min' or ind == 'tg_mean' or ind == 'tx_max':
                out = ds_means[k]-273.15
                out['p10'] = ds_means[k].quantile(q=0.1, axis = 1) - 273.15
                out['Median'] = ds_means[k].quantile(q=0.5, axis = 1) - 273.15
                out['p90'] = ds_means[k].quantile(q=0.9, axis = 1) - 273.15
            elif ind=='ice_days' or ind=='frost_days' or ind=='txgt_25' or ind=='txgt_30' or ind=='txgt_32' or ind=='tr_22' or ind=='tr_20' or ind=='gddgrow5' :
                out = ds_means[k] / np.timedelta64(1, 'D')
                out['p10'] = ds_means[k].quantile(q=0.1, axis = 1) / np.timedelta64(1, 'D')
                out['Median'] = ds_means[k].quantile(q=0.5, axis = 1)/ np.timedelta64(1, 'D')
                out['p90'] = ds_means[k].quantile(q=0.9, axis = 1)/ np.timedelta64(1, 'D')
            else:
                out= ds_means[k]
                out['p10'] = ds_means[k].quantile(q=0.1, axis = 1)
                out['Median'] = ds_means[k].quantile(q=0.5, axis = 1)
                out['p90'] = ds_means[k].quantile(q=0.9, axis = 1)
            out.to_csv(outfile)


        print('It took', (time.time() - start) / 60.0, 'minutes.')
        print('done')