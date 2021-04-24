# Add in modules
import os
import warnings
import glob
import matplotlib.pyplot as plt
import numpy.ma as ma
import xarray as xr
import rioxarray as rxr
from shapely.geometry import mapping, box
import geopandas as gpd
import earthpy as et
import earthpy.plot as ep
import gdal
from gdalconst import GA_ReadOnly
import rasterio as rio
from rasterio.plot import plotting_extent
import earthpy.spatial as es
from WBT.whitebox_tools import WhiteboxTools
wbt = WhiteboxTools()

# can be used once the code is written and working to stop warnings popping up to the user
# warnings.simplefilter('ignore')

from osgeo import gdal, osr
import numpy as np
from datetime import datetime
import sys, getopt, argparse, re

# check if working directory exists
scene_path = os.path.join("/SRS_Processing_Data")
if os.path.exists(scene_path):
    print('Data directory exists, all OK')
else:
    print('Create directory (C:\SRS_Processing_Data) and add multispectral scene for processing into this folder')

# Open hdf file, convert at sensor radiamce to top of atmosphere reflectance and create .tif files for each band
os.system("python ASTERL1T_DN2REF.py C:/SRS_Processing_Data/")

output_scene_path = os.path.join("/SRS_Processing_Data", 'output')


#Make a list of all the reflectance .tif file names and sort by band number
ASTER_band_list = [i for i in os.listdir(output_scene_path) if os.path.isfile(os.path.join(output_scene_path,i)) and \
                   'reflectance' in i]
ASTER_band_list.sort()
#print(ASTER_band_list)

# Alternative way of making list with path and filename
ASTER_band_list_path = glob.glob(os.path.join(output_scene_path, '*reflectance.tif'))
ASTER_band_list_path.sort()
#print(ASTER_band_list1)

# Simplify names for bands
b1 = ASTER_band_list_path [0]
print(b1)
b2 = ASTER_band_list_path [1]
b3 = ASTER_band_list_path [2]
b4 = ASTER_band_list_path [3]
b5 = ASTER_band_list_path [4]
b6 = ASTER_band_list_path [5]
b7 = ASTER_band_list_path [6]
b8 = ASTER_band_list_path [7]
b9 = ASTER_band_list_path [8]

# not working - arr_st, meta = es.stack(ASTER_band_list_path)

# Resample bands to same resolution using white box tools nn = nearest neighbour, shifts pixel by half pixel size
""" wbt.resample(
    b7,
    (b7 + '_resampled_WBT.tif'),
    cell_size=None,
    base=b1,
    method="nn",
)
"""

# Resample bands to same resolution, does the same as above but does not shift the pixel location
gdal.Warp((b7 + '_resampled_gdal.tif'), b7, xRes=15, yRes=15)

# Crop/clip images to b1 size
clipArea = gdal.Open(b1, GA_ReadOnly)
projection=clipArea.GetProjectionRef()
geoTransform = clipArea.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * clipArea.RasterXSize
miny = maxy + geoTransform[5] * clipArea.RasterYSize

data=gdal.Open('C:\SRS_Processing_Data\output\AST_L1T_00303052001084132_20150501094701_93840_ImageData7_reflectance.tif_resampled_gdal.tif', GA_ReadOnly) #Your data the one you want to clip ##need to add in here the path to the file
output=(str(output_scene_path) + '\output.tif') #output file
gdal.Translate(output,data,format='GTiff',projWin=[minx,maxy,maxx,miny],outputSRS=projection)

"""# Open bands in GDAL as datasets 'db1'
db1 = gdal.Open(b1)
db2 = gdal.Open(b2)
db3 = gdal.Open(b3)
db4 = gdal.Open(b4)
db5 = gdal.Open(b5)
db6 = gdal.Open(b6)
db7 = gdal.Open(str(output_scene_path) + '\output.tif')
db8 = gdal.Open(b8)
db9 = gdal.Open(b9)

#After hours of trying to get this to work realised this was not for Python
#gdalbuildvrt separate, stack.vrt, b7, b2, b1
#plt.imshow stack.vrt
#gdal_translate (stack.vrt, 7-2-1.tif)

print('Number of Raster Bands in image = ' + str(db1.RasterCount))

# False Colour Composite 7-2-1
# Fetch bands
band7 = db7.GetRasterBand(1)
band2 = db2.GetRasterBand(1)
band1 = db1.GetRasterBand(1)

# Read bands as Numpy arrays
a7 = band7.ReadAsArray()
a2 = band2.ReadAsArray()
a1 = band1.ReadAsArray()

# Plot the arrays
img721 = np.dstack((a7, a2, a1))
f = plt.figure()
plt.imshow(img721)
plt.savefig('721_fig.tif') # Saves low resolution figure of the plot
plt.show()
"""

band1=rio.open(b1)
print('Band 1 metadata ', band1.meta)
band2=rio.open(b2)
band7=rio.open(str(output_scene_path) + '\output.tif')

_721=rio.open('ASTER_721.tiff', 'w', driver='Gtiff',
                        width=band1.width, height=band1.height,
                        count=3,
                        crs=band1.crs,
                        transform=band1.transform,
                        dtype='float32',
                        nodata= 0.0)
_721.write(band7.read(1),1)
_721.write(band2.read(1),2)
_721.write(band1.read(1),3)
_721.close()






