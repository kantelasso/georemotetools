# -*- coding: utf-8 -*-
"""
Created on Sun May 14 14:46:24 2020

@author: Lancine KANTE
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import landsat as lsat

lsa=lsat.Landsat8()
today_path=lsa.get_nvisite()
gn=lsa.gn
#gn=gn[gn.DayNight=='DAY']

gn=gn[gn.ADate.between('02/01/2020','02/16/2020')]
xs = np.array(gn.loc[:,'CenterLongdec'])
ys = np.array(gn.loc[:,'CenterLatdec'])

def update_line(num, xs, ys, line,anime=False):
    if True==anime:
        line.set_xdata(xs[..., :num])
        line.set_ydata(ys[..., :num])
    else:
        line.set_xdata(xs)
        line.set_ydata(ys)
    return line,

nframe=len(gn.LPID.unique())

fig = plt.figure()
fig.add_subplot(111)
l, = plt.plot([], [], 'o',color='k',markersize=2,alpha=0.1)
plt.xlim(xs.min(),xs.max())
plt.ylim(ys.min(),ys.max())
line_static = FuncAnimation(fig, update_line, nframe, fargs=(xs, ys, l, False),
                                   interval=10)

# -----------------------------------------------------------------------------
# Real time visite of landsat 8
# -----------------------------------------------------------------------------
# Create new Figure and an Axes which fills it.

wrs=pd.read_csv('./data/WRS2_descending.csv')
wrs=wrs[wrs.PATH.isin(today_path)]
xs = np.array(wrs.loc[:,'CenterLong'])
ys = np.array(wrs.loc[:,'CenterLat'])

fig.add_subplot(111)
n_drops = len(xs)
# Create satelite characteristic
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

rain_drops['position'][:, 0] = xs
rain_drops['position'][:, 1] = ys
rain_drops['growth'] = np.linspace(15, 5, n_drops)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = plt.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=rain_drops['size'], lw=0.1, edgecolors=rain_drops['color'],
                  facecolors='r')

def update(frame_number):
    # Get an index which we can use to re-spawn the oldest point.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles smaller.
    rain_drops['size'] -= rain_drops['growth']

    # Pick a new position for oldest satelite position,
    #resetting its size and growth factor.
    rain_drops['size'][current_index] = 15
    rain_drops['growth'][current_index] = 5

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=50)

line, = plt.plot([], [], 'o',color='g',markersize=1,alpha=0.5)
nframe=len(wrs)/len(today_path)
nfr=len(wrs)
line_anime = FuncAnimation(fig, update_line, nfr, fargs=(xs, ys, line, True),
                                   interval=50)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Today Paths: %s [ * Landsat real time fly * ]'%(today_path))
#fig.tight_layout()
plt.show()
