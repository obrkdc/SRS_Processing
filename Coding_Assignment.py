# Add in modules
import os
import warnings

import matplotlib.pyplot as plt
import numpy.ma as ma
import xarray as xr
import rioxarray as rxr
from shapely.geometry import mapping, box
import geopandas as gpd
import earthpy as et
import earthpy.plot as ep

# can be used once the code is written and working to stop warnings popping up to the user
# warnings.simplefilter('ignore')

from osgeo import gdal, osr
import numpy as np
from datetime import datetime
import os, glob, sys, getopt, argparse, re

# check if working directory exists
scene_path = os.path.join("/SRS_Processing_Data")
if os.path.exists(scene_path):
    print('Data directory exists, all OK')
else:
    print('Create directory (C:\SRS_Processing_Data) and add multispectral scene for processing into this folder')

os.system("python ASTERL1T_DN2REF.py C:/SRS_Processing_Data/")

