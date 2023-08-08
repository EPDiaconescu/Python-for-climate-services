import xclim.ensembles as ensembles
import xclim.subset as subset
import xarray as xr
import glob
import os
from distributed import Client
import calendar
import numpy as np


def main():
    #client = Client(n_workers=4)
    indices = ['nr_cdd']
    rcps = ['rcp85']
    freq = ['YS']
    inpath = r'P:\30. CLIMATE SERVICES DATA PRODUCTS OFFICE\03 - Data, Code & Models\01 - Data\data_UNECE_nr'
    outpath = r'C:\Users\PomeroyC\Desktop\pct_UNEC'
    mods = ['BNU-ESM', 'CCSM4', 'CESM1-CAM5', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 
            'CanESM2', 'FGOALS-g2', 'GFDL-CM3', 'GFDL-ESM2G','GFDL-ESM2M', 
            'HadGEM2-AO','HadGEM2-ES', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 
            'MIROC-ESM-CHEM', 'MIROC-ESM', 'MIROC5', 'MPI-ESM-LR','MPI-ESM-MR',
            'MRI-CGCM3', 'NorESM1-M', 'NorESM1-ME', 'bcc-csm1-1-m', 'bcc-csm1-1']

    for f in freq:
        for i in indices:
            for r in rcps:
                ncfiles = []
                for m in mods:
                    file1 = sorted(glob.glob(os.path.join(inpath,f'*{m}_historical+{r}_r1i1p1_1950-2100_{i}_{f}.nc')))
                    ncfiles.extend(file1)
                outfile = f'BCCAQv2+ANUSPLIN300_ensemble-percentiles_historical+{r}_1950-2100_{i}_{f}.nc'
                list1  = []
                for nc in ncfiles:
                    ds1 = xr.open_dataset(nc, decode_times=False, chunks={'time':10})
                    ds1['time'] = xr.decode_cf(ds1).time
                    # subset for now
#                    list1.append(subset.subset_bbox(ds1, lon_bnds=[-80, -70], lat_bnds=[45, 50]))
                    list1.append(ds1)
                    del ds1
                # modify with total number of simulations
                if len(list1) == 24:
                    list1
                    ens = ensembles.create_ensemble(list1)
                    window = 10
                    time1 = xr.decode_cf(ens).time[0::window]
                    ens10y = ens.coarsen(time=window, boundary='trim').mean()
                    ens10y['time'] = time1[0:len(ens10y.time)]

                    for v in ens.data_vars:
                        ens = ens.rename({v: f'{r}_{v}'})
                        ens10y = ens10y.rename({v: f'{r}_{v}'})
                    if f == 'YS':

                        dims = list(ens.dims)

                        # with ProgressBar():
                        perc = (10, 50, 90)
                        for p in perc:
                            if p == perc[0] and r == rcps[0]:
                                mode = 'w'
                            else:
                                mode = 'a'

                            out = ensembles.ensemble_percentiles(ens, values=[p], time_block=30)

                            var = list(out.data_vars)
                            dims = list(out[list(out.data_vars)[0]].dims)

                            dims = list(out[list(out.data_vars)[0]].dims)
                            chunks = [1, 1, 1]
                            ii = dims.index('time')
                            chunks[ii] = len(out.time)
                            comp = dict(chunksizes=chunks)
                            encoding = {var: comp for var in out.data_vars}
                            encoding['time'] = dict(dtype='double')

                            print('writing to .nc file ', outfile)
                            out.to_netcdf(os.path.join(outpath,outfile), mode=mode, format='NETCDF4', encoding=encoding)
                            print('done p=',p)

                            if p == 50:
                                if r == rcps[0]:
                                    mode = 'w'
                                else:
                                    mode = 'a'
                                outfile1 = f'10yAvg_{outfile}'
                                out = ensembles.ensemble_percentiles(ens10y, values=[p], time_block=30)

                                var = list(out.data_vars)
                                dims = list(out[list(out.data_vars)[0]].dims)

                                dims = list(out[list(out.data_vars)[0]].dims)
                                chunks = list(out[list(out.data_vars)[0]].shape)
                                ii = dims.index('time')
                                chunks[ii] = 1
                                comp = dict(chunksizes=chunks)
                                encoding = {var: comp for var in out.data_vars}
                                encoding['time'] = dict(dtype='double')

                                print('writing to .nc file ',outfile1)
                                out.to_netcdf(os.path.join(outpath, outfile1), mode=mode, format='NETCDF4',
                                              encoding=encoding)
                                print('done, p=', p)

                    elif f == 'MS':
                        ensSub = ens
                else:
                    print("not 24 simulations in the ensembele; please verify")

if __name__ == "__main__": main()





