import numpy as np
import Tkinter as tk

import matplotlib
import patientsentiment
from patientsentiment import returnPoints
matplotlib.use('TkAgg')

from scipy.interpolate import spline

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pylab
import scipy.signal as signal
import numpy

fig = plt.figure()
fig.suptitle('Compression Velocity(mm/s)/Electrocardiogram Output(V)')
plt1 = fig.add_axes([0.1, 0.5, 0.8, 0.4],
                   xticklabels=[], ylim=(-400,0))
plt2 = fig.add_axes([0.1, 0.1, 0.8, 0.4],
                   ylim=(-1.2, 1.2))
handVelPoints = patientsentiment.returnPoints()
axisPts = [i for i in range(len(handVelPoints))]
plt1.plot(handVelPoints)


waves = signal.wavelets.daub(10) #daubechies wavelets
pause = numpy.zeros(10, dtype=float)
wavesFinal= numpy.concatenate([waves,pause])
heartRate = 60
beats= int(10 * heartRate / 60)

vitalsMonitor= numpy.tile(wavesFinal , beats)
plt2.plot(vitalsMonitor)


plt.show()
