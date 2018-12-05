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


suspoint = (0,25,0)
string = cylinder(pos = suspoint, axis =ball.pos-suspoint, radius = 0.1,
                  color = color.white)

length = abs(ball.pos- suspoint)
angularVelocity= 0
curr = 0
change = 0.01
#Lcostheta: difference between ball's height and string height
angle = math.acos(abs(suspoint[1]-ball.pos[1])/length)


while True:

    rate(350)
    gravity = 9.81
    acc = gravity / length * -1 * math.sin(angle)
    angularVelocity = angularVelocity + (acc * change)
    angle= angle +(angularVelocity*change)
    ball.pos = (length * math.sin(angle), suspoint[1] - length * math.cos(
        angle),0)
    newHeight = ball.pos-string.pos
    string.axis = newHeight
    curr+=change
    c = Leap.Controller()
    frame = c.frame()
    c.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    hand = frame.hands[0]
    for gesture in frame.gestures():
        if gesture.type is Leap.Gesture.TYPE_SWIPE:
            print('swipeeeeeee')
            swipe = Leap.SwipeGesture(gesture)
            swipeX = swipe.direction[0]
            current = swipe.position
            start = swipe.start_position
            motion = abs(current[0]-start[0])/100

            if swipeX<0:
                changeAng = swipe.speed/10000
                if angle+changeAng<=1.57:
                    angle+=changeAng

            elif swipeX>0:
                changeAng = swipe.speed / 10000
                if angle-changeAng>=-1.57:
                    angle -= changeAng