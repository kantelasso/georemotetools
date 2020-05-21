"""
===================
Saving an animation
===================

This example showcases the same animations as `basic_example.py`, but instead
of displaying the animation to the user, it writes to files using a
MovieWriter instance.
"""
# Source: https://matplotlib.org/gallery/animation/basic_example_writer_sgskip.html
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#%run landsat.py
#import landsat as lsat
#lsa=lsat.Landsat8()
gn=lsa.import_data(data='world')
gn=gn[gn.DayNight=='DAY']

def update_line(num, xs, ys, line):
    line.set_xdata(xs[..., :num])
    line.set_ydata(ys[..., :num])
    return line,


nframe=len(gn.LPID.unique())
xs = np.array(gn.loc[:,'CenterLongdec'])
ys = np.array(gn.loc[:,'CenterLatdec'])

fig = plt.figure()
fig.add_subplot()
l, = plt.plot([], [], 'o',color='b',markersize=2,alpha=0.2)
plt.xlim(xs.min(),xs.max())
plt.ylim(ys.min(),ys.max())
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Landsat fly path')
line_ani = animation.FuncAnimation(fig, update_line, nframe, fargs=(xs, ys, l),
                                   interval=50, blit=True)