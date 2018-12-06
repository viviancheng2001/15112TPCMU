
###############################################################################
# CITATION: Uses matplot lib libraries/functions to simulate ECG monitor as
# well as graph the user's hand compression velocity
###############################################################################

import numpy as np
import Tkinter as tk

import matplotlib
import Rescue
from Rescue import returnPoints
matplotlib.use('TkAgg')

from scipy.interpolate import spline

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pylab
import scipy.signal as signal
import numpy

fig = plt.figure()
fig.suptitle('Compression Velocity(mm/s)/Electrocardiogram Output(V)')
plt1 = fig.add_axes([0.1, 0.5, 0.8, 0.4],
                   xticklabels=[], ylim=(-400,0))
plt2 = fig.add_axes([0.1, 0.1, 0.8, 0.4],
                   ylim=(-1.2, 1.2))
handVelPoints = Rescue.returnPoints()
axisPts = [i for i in range(len(handVelPoints))]
plt1.plot(handVelPoints)

###############################################################################
# CITATION: Built-in daubechie wavelet from matplotlib library  used to
# simulate ECG waves/pauses for heartrate


heartRate = 60 #average person's
beats= int(10 * heartRate / 60) #heartbeats per second
waves = signal.wavelets.daub(10) #daubechies wavelets

pause = numpy.zeros(10, dtype=float)
wavesFinal= numpy.concatenate([waves,pause])
vitalsMonitor= numpy.tile(wavesFinal , beats)
plt2.plot(vitalsMonitor)
plt.show()
