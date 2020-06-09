# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:46:24 2020
@author: Lancine KANTE
"""
#%matplotlib inline
import landsat as lsat
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

lsa=lsat.Landsat8()
today_path=lsa.get_nvisite()
gn=lsa.gn[lsa.gn.DayNight=='DAY']

gn=gn[gn.ADate.between('02/01/2020','02/16/2020')]
xs = np.array(gn.loc[:,'CenterLongdec'])
ys = np.array(gn.loc[:,'CenterLatdec'])

def update_sat(num, xs, ys, line,anime=False):
    if True==anime:
        line.set_xdata(xs[..., :num])
        line.set_ydata(ys[..., :num])
    else:
        line.set_xdata(xs)
        line.set_ydata(ys)
    return line,

nframe=len(gn.LPID.unique())

fig, ax = plt.subplots()
ax.set_xlim(-180,180) # Limit of longitude
ax.set_ylim(-90,90) # Limit of latitude
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('* Landsat 8 flying path for dotay * See the paths list below \n %s'%(today_path))

l, = plt.plot([], [], 'o',color='k',markersize=2,alpha=0.1)
#Global taked scene by landsat 8
sat_taked = FuncAnimation(fig, update_sat, nframe, fargs=(xs, ys, l, False), interval=2)

# -----------------------------------------------------------------------------
# Real time visite of landsat 8
# -----------------------------------------------------------------------------
# Create new Figure and an Axes which fills it.

wrs=pd.read_csv('./data/WRS2_descending.csv')
wrs=wrs[wrs.PATH.isin(today_path)]
xs = np.array(wrs.loc[:,'CenterLong'])
ys = np.array(wrs.loc[:,'CenterLat'])

n_points = len(xs)
# Create satelite characteristic
satellite = np.zeros(n_points, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

satellite['position'][:, 0] = xs
satellite['position'][:, 1] = ys
satellite['growth'] = np.linspace(15, 5, n_points)

# Construct the scatter which we will update during animation
# as the satellite moves.
scat = plt.scatter(satellite['position'][:, 0], satellite['position'][:, 1],
                  s=satellite['size'], lw=0.1, edgecolors=satellite['color'],
                  facecolors='r')

def update(frame_number):
    # Get an index which we can use to re-spawn the oldest point.
    current_index = frame_number % n_points

    # Make all colors more transparent as time progresses.
    satellite['color'][:, 3] -= 1.0/len(satellite)
    satellite['color'][:, 3] = np.clip(satellite['color'][:, 3], 0, 1)

    # Make all circles smaller.
    satellite['size'] -= satellite['growth']

    # Pick a new position for oldest satelite position,
    #resetting its size and growth factor.
    satellite['size'][current_index] = 15
    satellite['growth'][current_index] = 5

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_sizes(satellite['size'])
    scat.set_offsets(satellite['position'])

# Construct the animation, using the update function as the animation director.
sat_animation = FuncAnimation(fig, update, interval=10)

#Satellite real position in read
line, = plt.plot([], [], 'o',color='g',markersize=1,alpha=0.5)

#Plot satellite trace in green color
sat_trace = FuncAnimation(fig, update_sat, len(wrs), fargs=(xs, ys, line, True), interval=10)

plt.show()