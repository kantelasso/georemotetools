# -*- coding: utf-8 -*-
"""
Created on Thu May 14 05:58:25 2020

@author: hp
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x_data = []
y_data = []

fig, ax = plt.subplots()
ax.set_xlim(0,105)
ax.set_ylim(0,12)
line, = ax.plot(0,0,marker='o')

def animation_frame(i):
    x_data.append(i*10)
    y_data.append(i)

    line.set_xdata(x_data)
    line.set_ydata(y_data)
    return line,

animation = FuncAnimation(fig, func=animation_frame,
                          frames=np.arange(0,10,0.01),interval=10)
plt.show()