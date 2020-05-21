# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:16:46 2018
@author: USER
"""

faults = """
140, 90 NW
55, 90
145, 65 W
110, 0 NW
90, 90
10, 90
115, 90
140, 60 SW
75, 80 SW
170, 70 W
0, 50 W
95, 50 SE
110, 85 NE
50, 50 SE
110, 85 NE
150, 85 NE
150, 85 NE
50, 50 SE
100, 80 SW
85, 90 NW
50, 65 SE
80, 85 NW
150, 90
138, 60 SW
100, 74 S
118, 70 N
120, 90
130, 90
130, 90
110, 90
35, 70 SE
70, 60 NW
60, 80 NW
150, 90
70, 70 NW
70, 75 NW
100, 75 SW
82, 70 SW
45, 70 NW
35, 40 NW
40, 75 SE
90, 50 S
85, 60 S
50, 85 SE
20, 56 W
76, 80 S
140, 60 SW
80, 40 N
115, 64 NE
150, 60 SE
70, 68 SE
70, 70 SE
50, 45 SE
84, 80 N
92, 56 S
110, 90
80, 90
110, 90
110, 80 S
110, 55 N
80, 50 N
110, 80 N
0, 90
60, 90
130, 90
130, 90
130, 90
140, 90
60, 90
60, 90
45, 60 NW
30, 90
100, 80 S
30, 30 NW
60, 90
30, 30 SE
85, 60 S
70, 90
10, 80 W
55, 80 SE
95, 70 S
80, 65 S
160, 30 E
50, 85 SE
150, 48 NE
100, 30 NE
120, 80 SW
70, 64 N
170, 70 W
90, 80 S
90, 80 S
108, 70 SW
160, 85 E
120, 68 SW
160, 70 SW
160, 30 NE
40, 60 SE
30, 50 SE
85, 50 SE
35, 50 SE
135, 50 NE
110, 50 NE
140, 45 NE
145, 78 SW
145, 38 SW
100, 70 SW
30, 60 NW
160, 60 SE
110, 60 SE
104, 80 SW
130, 60 SW
110, 80 SW
120, 50 SW
145, 72 SW
110, 50 NE
150, 40 NE
145, 24 SW
100, 30 N
130, 30 N
100, 40 N
105, 80 S
105, 50 S
115, 50 S
110, 55 S
150, 85 W
40, 60 N
32, 60 N
40, 80 N
160, 60 SW
160, 74 SW
130, 72 SW
150, 60 SW
140, 32 N
80, 80 N
60, 78 N
70, 80 N
75, 90
150, 86 N
40, 90
45, 90
40, 90
40, 90
150, 80 N
170, 72 N
"""

bdk_faults = """
75, 80 SW
0, 50 W
95,50 SE
50,50 SE
50,50 SE
100,75 SW
82,70 SW
45,70 NW
140,60 SW
80,40 N
115,64 NE
150,60 SE
160,30 NE
40,60 SE
140,45 NE
145,38 SW
100,70 SW
30,60 NW
160,60 SE
110,60 SE
104,80 SW
130,60 SW
110,80 SW
120,50 SW
145,72 SW
110,50 NE
150,40 NE
145,24 SW
100,30 N
130,30 N
100,40 N
105,80 S
105,50 S
115,50 S
110,55 S
150,85 W
5,0 W
5,0 W
0,0 W
0,0 W
"""

bdk_fault_mine = """
120, 50	SW
105, 50	S
150, 60	SE
110, 80	SW
100, 70	SW
100, 40	N
150, 85	W
5, 0	W
130, 60	SW
145, 72	SW
145, 24	SW
"""

trik = """
120,80 NE
155,85 E
50,50 NW
114,70 NE
130,60 NE
100,80 NW
10,80 E
120,85 NE
150,80 NE
120,80 NE
105,80 NE
120,80 NE
130,82 NE
95,80 NE
50,80 NE
30,70 W
10,75 W
150,75 SW
152,70 SW
140,70 SW
140,75 SW
88,80 S
120,60 SW
120,70 SW
60,65 S
70,70 S
70,70 S
70,70 S
70,75 S
70,65 S
140,80 SW
160,85 W
160,85 W
40,85 N
70,85 N
130,70 SW
20,80 W
125,70 SW
170,85 W
170,85 W
170,85 W
170,85 W
180,85 W
10,85 E
10,85 E
5,85 E
5,85 E
5,85 E
5,85 E
145,72 SW
110,80 SW
120,50 SW
145,38 SW
5,80 E
130,60 SW
100,40 N
145,70 SW
10,85 E
165,80 W
172,52 E
168,70 E
152,64 E
100,60 NE
60,80 S
46,64 NW
60,70 N
120,48 SW
134,42 SW
12,64 W
12,54 W
150,85 SW
90,78 S
30,70 SE
37,70 SE
44,64 SE
"""

import numpy as np
import mplstereonet
import matplotlib.pyplot as plt


#Transforme fault to dip/trende data
#
#strikes, dips = zip(*[mplstereonet.parse_strike_dip(*s.strip().split(','))
#for s in faults.split('\n') if s])

#strikes, dips = zip(*[mplstereonet.parse_strike_dip(*s.strip().split(','))
#for s in bdk_faults.split('\n') if s])

#strikes, dips = zip(*[mplstereonet.parse_strike_dip(*s.strip().split(','))
#for s in bdk_fault_mine.split('\n') if s])

strikes, dips = zip(*[mplstereonet.parse_strike_dip(*s.strip().split(','))
for s in trik.split('\n') if s])


strikes, dips

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111,projection='stereonet')
ax.plane(strikes,dips,c='k',label='Fault system')
strike, dip = mplstereonet.fit_girdle(strikes,dips)
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
#fig = plt.figure(figsize=(15,7))
fig = plt.figure(figsize=(8,8))
#ax = fig.add_subplot(121,projection='stereonet')
ax = fig.add_subplot(111,projection='stereonet')
ax.pole(strikes,dips,c='k',label='Pole of Faults Planes')
ax.density_contourf(strikes,dips,mesurement='poles',cmap='Reds')

#ax.set_title('Density contour of the "Faults system" Poles', y=1.10, fontsize=15)
#ax.grid()

ax.set_title('Contour de densite des poles des veines', y=1.10, fontsize=15)
ax.grid()


fig = plt.figure(figsize=(8,8))
#ax = fig.add_subplot(122,projection='polar')
ax = fig.add_subplot(111,projection='polar')
ax.bar(np.deg2rad(np.arange(0,360,10)),two_halves,
    width=np.deg2rad(10),bottom=0.0,color='.8',edgecolor='k')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_thetagrids(np.arange(0,360,10),labels=np.arange(0,360,10))
ax.set_rgrids(np.arange(1,two_halves.max()+1,2), angle=0,weight='black')
#ax.set_title('Rose diagram of "Faults system"', y=1.10,fontsize=15)
ax.set_title('Diagramme rose des veines', y=1.10,fontsize=15)
fig.tight_layout()
#fig

