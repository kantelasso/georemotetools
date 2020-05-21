
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

gn=gn[gn.ADate.between('04/01/2013','04/02/2013')]
xs = np.array(gn.loc[:,'CenterLongdec'])
ys = np.array(gn.loc[:,'CenterLatdec'])

# Create new Figure and an Axes which fills it.
fig = plt.figure()
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)
#ax = fig.add_subplot(111)
#ax.set_xlim(xs.min(),xs.max())
#ax.set_ylim(ys.min(),ys.max())

# Create rain data
n_drops = len(xs)
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
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] -= rain_drops['growth']

    # Pick a new position for oldest rain drop, resetting its size,
    # color and growth factor.
    rain_drops['size'][current_index] = 15
    rain_drops['color'][current_index] = (0, 0, 0, 1)
    rain_drops['growth'][current_index] = 5

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=50)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()
