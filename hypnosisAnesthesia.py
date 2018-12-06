
###############################################################################

# CITATION: Created using outline of providedStarterFile leapMotionDemo.py
# which includes:
# LeapMotion built-in variables/gesture-detection functions from leap
# motion library
# 112 Tkinter Framework, from the CMU 15-112 course
# Uses Vpython's built-in functions and library, a module that allows for
# better visualization of objects.

#Implements functions from leapMotion database to obtain hand data
###############################################################################
from visual import *
import math

import Leap, sys, thread, time
import sys

sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")
from Leap.Other import Leap
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk



########### setup bob, pendulum ##############
scene.width = 700
scene.height = 600

im = Image.open('images/clk.jpg')  # size must be power of 2, ie 128 x 128
clock = materials.texture(data=im, mapping='sign')

ball = sphere(pos=[3, 1, 0], material=clock, radius=3, axis=[0, 0, 1])
countOsc = 0

T = text(text='Hypnosis, a new form of anesthesia',
         align='center', pos=(0, -5, 0), color=(1, 0.7, 0.2),
         linecolor=color.red,
         height=3)

# SETUP Pt 2: Declare variables to Simulate a moving pendulum #
suspoint = (0, 25, 0)
string = cylinder(pos=suspoint, axis=ball.pos - suspoint, radius=0.1,
                  color=(1, 0.7, 0.2))
length = abs(ball.pos - suspoint) #difference of ball's position and
# suspension point
angularVelocity = 0
gravity = 9.81 #gravity
centimeters = length * 2.54 / 96 #convert pixels to cm
period = 2 * math.pi * math.sqrt(abs(centimeters / gravity)) #T = 2pi (sqrt(
# L/g))
curr = 0
change = 0.01 #change in time
# Lcostheta: difference between ball's height and string height
angle = math.acos(abs(suspoint[1] - ball.pos[1]) / length)


L = label(pos=(0, 4, 0),
          text="Pendulum period is " + str(period) + " seconds per "
                                                     "oscillation")
label(pos=(0, 7, 0), text="Use hand to change oscillation")
#use time.time() to calculate oscillations/s through time elapsed and number of
#  oscillations counted
t1 = time.time()


#endless loop
while True:
    rate(350)
    acc = gravity / length * -1 * math.sin(angle) #acceleration formula based
    #  on gravity and angle
    angularVelocity = angularVelocity + (acc * change) #w=w0 + at
    angle = angle + (angularVelocity * change) #theta = theta+wt
    #update ball position
    ball.pos = (length * math.sin(angle), suspoint[1] - length * math.cos(
        angle), 0)
    newHeight = ball.pos - string.pos
    #update string's angle/position
    string.axis = newHeight
    #update time
    curr += change

    #####LEAP MOTION to manually play around with around pendulum motion######
    c = Leap.Controller()
    frame = c.frame()
    hand = frame.hands[0]

    #check hand palm velocity and use that to change the angle of pendulum
    vel = hand.palm_velocity[0]
    angle += vel / 100000
    bottomPoint = suspoint[1] - (length * math.cos(0))
    if abs(ball.pos[1] - bottomPoint) < 0.000025:
        countOsc += 1
        print(countOsc)
        #count oscillations, divide by seconds elapsed
        diff = abs(t1 - time.time())
        print(diff)
        period = (diff / countOsc)
    L.text = "Pendulum period is " + str(period) + " seconds per oscillation"
