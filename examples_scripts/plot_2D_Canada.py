

from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib  as mpl
from matplotlib.colors import Normalize
from scipy import *
import sys
import os

def mf1(data):
    return (float('{:.1f}'.format(data)))

def mf2(data):
    return (float('{:.2f}'.format(data)))


def plotP2(inCentral,lonCentral,latCentral,levels,tCentral,txtLabel,imgout):
    colors = mpl.colors.ListedColormap ([(0.0, 0.070588235294117674, 0.28627450980392155),
                                        (0.0, 0.14117647058823535, 0.4274509803921569),
                                        (0.0, 0.21176470588235285, 0.47450980392156861),
                                        (0.0, 0.35882352941176465, 0.5725490196078431),
                                        (0.0, 0.42941176470588238, 0.61960784313725492),
                                        (0.14117647058823524, 0.57058823529411762, 0.71372549019607845),
                                        (0.26013072828451794, 0.65098041296005249, 0.80000001192092896),
                                        (0.34117648005485535, 0.72156864404678345, 0.81568628549575806),
                                        (0.52941177090009051, 0.81777778863906858, 0.75294119119644165),
                                        (0.70588237047195435, 0.88496732711791992, 0.73071897029876709),
                                        (0.83137255907058716, 0.93411765098571775, 0.80705883502960207),
                                        [ 1.        ,  1.0,  1.0],
                                        [ 0.99607843,  0.87843137,  0.82352941],
                                        [0.99, 0.8, 0.7],
                                        [ 0.98823529,  0.73333333,  0.63137255],
                                        [ 0.98823529,  0.57254902,  0.44705882],
                                        [ 0.98431373,  0.41568627,  0.29019608],
                                        [ 0.9372549 ,  0.23137255,  0.17254902],
                                        [ 0.79607843,  0.09411765,  0.11372549],
                                        [ 0.64705882,  0.05882353,  0.08235294],
                                        [0.5, 0., 0.06],
                                        [ 0.40392157,  0.        ,  0.05098039],
                                        [0.2783814132520015, 0.0, 0.0]])
    norm = mpl.colors.BoundaryNorm(levels, len(levels)-1)
    f = plt.figure(figsize=(10,6))
#    ax1 = plt.subplots()
#    f.add_subplot(ax1)
    width = 6400000; height=4900000; lon_0 = -105; lat_0 = 64
    m = Basemap(width=width,height=height,resolution='l',projection='laea',lat_ts=65,lat_0=63,lon_0=-96.)
    m.drawcountries(linewidth=0.5)
    m.drawcoastlines(linewidth=0.5)
    m.drawlsmask(land_color='0.8', ocean_color=(0.77647059,  0.85882353,  0.9372549), lakes=True)
    x,y = m(lonCentral,latCentral)
    im=m.pcolormesh(x,y,inCentral,cmap=colors, latlon=False,norm=norm)
    plt.title(tCentral, size=18)
    c = plt.colorbar(im, fraction=0.046, pad=0.04, orientation='vertical', extend='both',extendfrac='auto')
    c.set_label(txtLabel, size=14)
    c.set_ticks(levels)
    font_size = 12 # Adjust as appropriate.
    c.ax.set_xticklabels(levels)
    c.ax.tick_params(labelsize=font_size)
    f.savefig(imgout, dpi=400)
    plt.close()


input= 'H:/ec2018/PCIC-test/netCDF_means20years/'
varName='tasmax'
for fld in os.listdir(input)[:]:
    print(fld)

    txtLabel='  '
    output='D:/ec2018/PCIC-test/figures_means20years/'+fld[:-3]+'.png'

    #####################################################################################################

    nc = Dataset(input+fld)
    lats0 = nc.variables['lat'][:]
    lons0 = nc.variables['lon'][:]
    lons0, lats0 = np.meshgrid(lons0, lats0)
    data0 = nc.variables[varName][:].squeeze()
    data0=data0
#    lons0 = lons0 - 360
    nc.close()



    val1=np.max([abs(np.min(data0)),abs(np.max(data0))])

    # if val1<1.0:
    #     valExt=mf2(val1)
    #     pasul=mf2(valExt/12)
    #     lev1=(((np.arange(pasul/2.0,25*pasul/2.0,pasul))*(-1))[::-1])
    #     lev2=np.arange(pasul/2.0,25*pasul/2.0,pasul)
    #     clevs=np.append(lev1,lev2)
    # elif val1<12.0:
    #     valExt=mf1(val1)
    #     pasul=mf1(valExt/12)
    #     lev1=(((np.arange(pasul/2.0,25*pasul/2.0,pasul))*(-1))[::-1])
    #     lev2=np.arange(pasul/2.0,25*pasul/2.0,pasul)
    #     clevs=np.append(lev1,lev2)
    # else:
    #     valExt=np.int(val1)
    #     pasul=valExt/12
    #     lev1=(((np.arange(pasul/2.0,25*pasul/2.0,pasul))*(-1))[::-1])
    #     lev2=np.arange(pasul/2.0,25*pasul/2.0,pasul)
    #     clevs=np.append(lev1,lev2)

    if fld[-9:]=='summer.nc':
        clevs = array([-33., -30., -27., -24., -21., -18., -15., -12., -9., -6., -3.,
                       -1., 1., 3., 6., 9., 12., 15., 18., 21., 24., 27.,
                       30., 33.])
    else:
        clevs=array([-23., -21., -19., -17., -15., -13., -11., -9., -7., -5., -3.,
               -1., 1., 3., 5., 7., 9., 11., 13., 15., 17., 19.,
               21., 23.])

    norm = mpl.colors.BoundaryNorm(clevs, len(clevs)-1)

    plotP2(data0,lons0,lats0,clevs,txtLabel,' ',output)


print('FINISH')
#####################################################################################################

