# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# # -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 22:32:50 2018

Update start on Thursday 19 March 2020
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
env.workspace = "C:/GeoTools/GeoStructure/"
# Enable overwriting
arcpy.env.overwriteOutput = True


# Run Module
%run GeoStereoModule.py
import GeoStereoModule as gts
outdir='C:/GeoTools/GeoStructure/Output/'
geo=gts.GeoStereo(outdir)
diraz=geo.dirToAz('Input/demo_data.csv',dipazimut=True)
dire=pd.DataFrame.from_csv('Input/demo_data.csv')
xytable='C:/GeoTools/GeoStructure/Input/DirazCalculated.csv'
geo.strikeToLine(xytable)
#geo.Stereo()

"""
# Script arguments
strpt = arcpy.GetParameterAsText(0) # Point input
x = arcpy.GetParameterAsText(1) # X coordinate
y = arcpy.GetParameterAsText(2) # Y coordinate
thn = arcpy.GetParameterAsText(3) # Thikness
proj = arcpy.GetParameterAsText(4) # CRS
outfol = arcpy.GetParameterAsText(5) # Output folder
"""
#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
# For merge feature class
#
# Create FieldMappings object to manage merge output fields
fieldMappings = arcpy.FieldMappings()
#field_usefull= ['Categorie','Lithology','Au_ppm']
field_usefull= ['id','Categorie','Lithology']
# Update here according to the vein structure feature class
#
stpts = xytable
strike=outdir+'St_Strike.shp'
fref='id'
arcpy.JoinField_management(in_data=strike,in_field=fref,
                           join_table=stpts,join_field=fref,
                           fields=field_usefull)
for fld in field_usefull:
    arcpy.AddField_management(Strike,fld)
    arcpy.CalculateField_management(Strike,fld,expression=)

##_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
#

# --------------------------------------------------------------------
""" *** *** Spatial distribution modeling *** ***
"""
shp_pt = r"D:\Managem\TriK_2019\Hassan\Exploration_2019\Structure\TriK_Exploration_Structure.shp"
lt,i = [],0
#for i in range(1127):
for i in range(64):
    a,b,c=arcpy.CalculateDistanceBand_stats(shp_pt,i+1,"EUCLIDEAN_DISTANCE")
    lt.append([i+1,float(a),float(b),float(c)])

df=pd.DataFrame(lt,columns=['N','Min','Mean','Max'])
#df.head()
#df.to_csv('C:/GeoTools/GeoStructure/Input/df.csv',header=True)
df.describe().round(0)
df.describe(percentiles=np.arange(0.01,0.21,0.01)).round()
