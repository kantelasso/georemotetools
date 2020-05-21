# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:57:29 2020
@author: Lancine KANTE
@email: kantemou@gmail.com
@startdate: 2020-03-20
"""
import arcpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplstereonet as mste

arcpy.env.workspace = "C:/GeoRemoteTools/geospatiale/"
arcpy.env.overwriteOutput = True # Enable overwriting existing file
#arcpy.env.outputCoordinateSystem = 'WGS 1984 UTM ZONE 29N'

# * * * * * Fonction to make object-oriented program * * * * *
class GeoStereo(object):
    """ Python and ArcPy Module that calculate some important paremeters of
    linear structure like geological structrure analysis and stereonet
    """
    def __init__(self,outdir,prj='WGS 1984 UTM ZONE 29N'):
        # Set environment settings and global variable
        self.prj = arcpy.SpatialReference(prj)
        self.pts = None
        self.outdir = outdir
        self.deletable_data = None

    def dirToAz(self,table,dipazimut=False,rule='right_hand_rule'):
        """Converte Direction of linear structure in Strike according to a right hand rule
        Input: (table,dipazimut,rule)
            table: tabular data like csv, excel, it may contain direction, dip and plunge of structure
            dipazimut: default False, does the structure data contain plunge to calculate dipazimut
            rule: default right_hand_rule, the methode to determinate strike of linear structure
        Output: tabular data with correct linear structutre
        """
        if table.endswith('.csv') or table.endswith('.txt'):
            pts = pd.read_csv(table) # Import csv data
        else:
            print 'Error, tabular data structure not reconized, Please import csv or excel file'

        aztxt = np.char.array(pts['az'].values) # converte azimut to text like 50 to 'N50'
        diptxt = np.char.array(pts['dip'].values) # converte dip to text like 50 to '50'
        pts['txt'] = aztxt + ',' + diptxt + pts.plg
        strikes,dips = zip(*[mste.parse_strike_dip(*s.strip().split(','))for s in pts.txt if s])
        pts['stk'] = strikes
        if True==dipazimut:
            # Calculate dipazimut according to the value of strike
            mask = pts.stk>270
            pts.loc[mask,'dipaz'] = pts.stk-270 # Where strike>270, dipaz = strike+90-360
            pts.loc[~mask,'dipaz'] = pts.stk+90 # Where strike<270, dipaz = strike+90-360
        self.pts = pts
        try:
            pts['ln'] = 5*pts['thn'] #calculate the length of polyline
            pts['lnc'] = -1*pts['ln'] #calculate the opposite length of polyline
            pts['dipln'] = 0.01+pts['ln']*(90-pts['dip'])*(0.5/90)
        except Exception as e:
            raise e
        # Export pts tabular data to csv file
        try:
            pts.to_csv('geospatiale/Input/DirazCalculated.csv')
            print "Your linear structure file is succesfully created"
            print "At  Input/DirazCalculated.csv' as tabular data"
            print 'Please check it and make change as you like'
        except Exception as e:
            raise e
        return self.pts

    def strikeToLine(self,xytable):
        """ Convert strike tabular data to shapefile polyline
        Input: xytable
            xytable: tabular data contain x and y coordinates
        Output: outdir
            outdir: directory or folder of output shapefile polyline
        """
        # Set coordinate system of future shapefile
        prj, outdir = self.prj, self.outdir

        # Import csv file already calculated by dirToAz method
        pt = "/Input/DirazCalculated.csv" # don't use pandas DataFrame as an input data
        # A dataframe that contain the caracteristic of different output shp file
        ft = pd.DataFrame([['ln','lnc','dipln','merge'],['stk','stk','dipaz','merge'],
                  ['St1.shp','St2.shp','DipAzimut.shp','St_Strike.shp']]
                  ,columns=['Measure1','Measure2','DipAz','Strike'])
        for i in range(len(ft)+1):
            if 'merge'==ft.iloc[0,i]:
                arcpy.Merge_management([outdir+ft.iloc[2,0],outdir+ft.iloc[2,1]],outdir+ft.iloc[2,3])
                arcpy.Dissolve_management(outdir+ft.iloc[2,3], outdir+"Direction.shp", "id", "",
                                          "MULTI_PART", "DISSOLVE_LINES")
                print '--- Your tabular data is converted in shapefile successfully !---'
            else:
                arcpy.BearingDistanceToLine_management(in_table=pt,
                                                out_featureclass=outdir+ft.iloc[2,i],
                                               x_field='x', y_field='y',
                                               distance_field=ft.iloc[0,i],distance_units="METERS",
                                               bearing_field=ft.iloc[1,i],bearing_units="DEGREES",
                                               line_type="GEODESIC",id_field='id',
                                               spatial_reference=prj)
        return


    def pointdensity(self,in_shp_pt,out_shp_pg):
        pass



    def Stereo(self):
        """ Stereographic representation function
        Determine the hight place density of structure,
        Calculate distributiion of structure and its characteristic (min, mean, max)
        """
        strikes,dips = self.pts['stk'],self.pts['dip']
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(111,projection='stereonet')
        ax.plane(strikes,dips,c='k',label='Fault system')
        strike, dip = mste.fit_girdle(strikes,dips)
        ax.pole(strike,dip,c='r',label='Pole of Fault plane')

        # Calculate the number of directions (strikes) every 10° using numpy.histogram
        bin_edges = np.arange(-5,366,10)
        number_of_strikes, bin_edges = np.histogram(strikes,bin_edges)

        # Sum the last value with the first value
        number_of_strikes[0] += number_of_strikes[-1]
        '''
        Sum the first half 0-180° with the second half 180-360° to achieve the
        "mirrored behavior" of Rose Diagrams
        '''
        half = np.sum(np.split(number_of_strikes[:-1],2),0)
        two_halves = np.concatenate([half,half])

        # Create the rose diagram
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111,projection='stereonet')
        ax.pole(strikes,dips,c='k',label='Pole of Structure Planes')
        ax.density_contourf(strikes,dips,mesurement='poles',cmap='Reds')

        ax.set_title('Pole Density contour of de Structure', y=1.10, fontsize=15)
        ax.grid()

        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111,projection='polar')
        ax.bar(np.deg2rad(np.arange(0,360,10)),two_halves,
               width=np.deg2rad(10),bottom=0.0,color='.8',edgecolor='k')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.arange(0,360,10),labels=np.arange(0,360,10))
        ax.set_rgrids(np.arange(1,two_halves.max()+1,2), angle=0,weight='black')
        ax.set_title('Rose Diagram of Structure', y=1.10,fontsize=15)
        fig.tight_layout()

