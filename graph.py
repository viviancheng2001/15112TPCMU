
import Surgery
import numpy as np
from Surgery import returnPoints
import matplotlib
matplotlib.use("TkAgg")
from scipy.interpolate import spline
from matplotlib import pyplot as plt


twistYawpts,twistRollpts, axispts = Surgery.returnPoints()

axisPts = [i for i in range(len(twistYawpts))]

#################    YAW    #############################

T = np.array(axisPts)
power = np.array(twistYawpts)

xnew = np.linspace(T.min(), T.max(), 300)
powerSmooth = spline(T, power, xnew)
plt.title("Hand Yaw")
plt.plot(xnew, powerSmooth, 'ro')

#
# fig = plt.figure()
# fig.suptitle('yaw', fontsize = 20)


# plt.axis([0,len(twistYawpts), -150,150])
# # line, = plt.plot(axisPts,twistYawpts, '-')
# # line.set_antialiased (True)
# # plt.ylabel('yaw')
# plt.show()


#################     ROLL       #############################


fig = plt.figure()
fig.suptitle('roll', fontsize = 20)

plt.plot(axisPts, twistRollpts, 'ro')
plt.axis([0,len(twistRollpts), -150,150])
line, = plt.plot(axisPts,twistRollpts, '-')
plt.ylabel('roll')
plt.show()