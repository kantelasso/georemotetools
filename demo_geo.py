# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# # -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 22:32:50 2018
Update start on Thursday 19 March 2020
Update on Thu Apr 23 00:30:41 2020
Update finished on

@author: Lancine KANTE
@email: kantemou@gmail.com
"""

# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy
from arcpy import env
import numpy as np
import pandas as pd

# Set environment settings
env.workspace = "C:/GeoRemoteTools/"
arcpy.env.overwriteOutput = True # Enable overwriting

# Import Run Module
%run geostereo.py
import geostereo as gts
outdir='C:/GeoRemoteTools/geospatiale/Output/'
geo=gts.GeoStereo(outdir)
diraz=geo.dirToAz('geospatiale/Input/demo_data.csv',dipazimut=True)
dire=pd.read_csv('geospatiale/Input/demo_data.csv')
xytable='C:/GeoRemoteTools/geospatiale/Input/DirazCalculated.csv'
geo.strikeToLine(xytable)
geo.Stereo()
