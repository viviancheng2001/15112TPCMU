from visual import*
import math

import Leap, sys, thread, time
import sys
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")
from Leap.Other import Leap
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk


scene.width=700
scene.height = 600

im = Image.open('images/clk.jpg')  # size must be power of 2, ie 128 x 128
clock = materials.texture(data=im, mapping='sign')

ball= sphere(pos = [3,1,0], material =clock, radius = 3, axis = [0,0,1])
countOsc = 0

T = text(text='Hypnosis',
     align='center',pos = (0,-5,0), color=(1,0.7,0.2),linecolor = color.red,
         height = 3)
suspoint = (0,25,0)
string = cylinder(pos = suspoint, axis =ball.pos-suspoint, radius = 0.1,
                  color = (1,0.7,0.2))
length = abs(ball.pos- suspoint)
angularVelocity= 0
gravity = 9.81
centimeters = length * 2.54/96
period = 2 * math.pi * math.sqrt(abs(centimeters / gravity))
curr = 0
change = 0.01
#Lcostheta: difference between ball's height and string height
angle = math.acos(abs(suspoint[1]-ball.pos[1])/length)


label(pos=(0,6,0), text="Use hand to change oscillation")
t1 = time.time()
L = label(pos=(0, 4, 0),
          text="Pendulum period is " + str(period) + " seconds per "
                                                     "oscillation")

#
# if abs(ball.pos[0]) <0.0015:
#     print('center')
while True:
    rate(350)
    acc = gravity / length * -1 * math.sin(angle)
    angularVelocity = angularVelocity + (acc * change)
    angle= angle +(angularVelocity*change)
    ball.pos = (length * math.sin(angle), suspoint[1] - length * math.cos(
        angle),0)
    newHeight = ball.pos-string.pos
    string.axis = newHeight
    curr+=change
    # print(angle)
    c = Leap.Controller()
    frame = c.frame()
    hand = frame.hands[0]

    vel = hand.palm_velocity[0]
    angle +=vel/100000
    #print(ball.pos[1])
    bottomPoint = suspoint[1]- (length*math.cos(0))
    #print(bottomPoint)
    if abs(ball.pos[1] - bottomPoint) <0.00001:
        countOsc +=1
        print(countOsc)
        diff = abs(t1 - time.time())
        print(diff)
        period = (diff/countOsc)
    L.text = "Pendulum period is " + str(period) + " seconds per oscillation"



    # c = Leap.Controller()
    # frame = c.frame()
    # c.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    # hand = frame.hands[0]
    # for gesture in frame.gestures():
    #     if gesture.type is Leap.Gesture.TYPE_SWIPE:
    #         print('swipeeeeeee')
    #         swipe = Leap.SwipeGesture(gesture)
    #         swipeX = swipe.direction[0]
    #         current = swipe.position
    #         start = swipe.start_position
    #         motion = abs(current[0]-start[0])/100
    #
    #         if swipeX<0:
    #             changeAng = swipe.speed/10000
    #             print(changeAng)
    #             if angle+changeAng<=1.57:
    #                 angle+=changeAng
    #
    #         elif swipeX>0:
    #             changeAng = swipe.speed / 10000
    #             if angle-changeAng>=-1.57:
    #                 angle -= changeAng