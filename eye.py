import Leap, sys, thread, time
import sys
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")
from Leap.Other import Leap
from Leap.Other.Leap import SwipeGesture
from Tkinter import *
from PIL import Image, ImageTk

import numpy as np

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


#User manipulates eyeball with hands through Leapmotion/Vpython; to win they
# need to remove a stye (red sphere) embedded into the eyeball.
from visual import *

scene.range = 5 #Sets Zoom Distance

scene.width = 500
scene.height = 500
scene.autocenter = True #Auto Centers Camera on Scene
ang = 0.005


#Create eyeball
im = Image.open('images/eyeNew.jpg')  # size must be power of 2, ie 128 x 128
tex = materials.texture(data=im, mapping='sign')
eyeball= sphere(pos = [0,0,0], material =tex, radius = 1)
v= vector(eyeball.radius,0,0)
e = sphere(color=
           color.red, pos=eyeball.pos + v, radius= \
               0.2)
eyeballSpeed = 0

#########Instructions
T = text(text='Fix the eye',
     align='center',pos = (0,4,0), color=color.green,linecolor = color.red)

label(pos=(0,3.5,0), text='Use hands to rotate eyeball and find the stye')
label(pos=(0,3.0,0), text='Stop eyeball motion by pressing any key')
label(pos=(0,2.5,0), text='Remove stye by clicking on it')

#Manipulate eyeball/stye dimensions
def zoom(eyeBallMoveable = True):
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    hand_speed = hand.palm_velocity
    #print(hand_speed[1])
    if eyeBallMoveable == True:
        if e.radius <= eyeball.radius/5:
            if hand_speed[1] <-50 and eyeball.radius >-2:
                eyeballSpeed = abs(hand_speed[1]) / 500000
                eyeball.radius -= eyeballSpeed
                e.radius -=eyeballSpeed
            elif hand_speed[1] > 50 and eyeball.radius < 4:
                eyeballSpeed = abs(hand_speed[1]) / 500000
                eyeball.radius +=eyeballSpeed
                e.radius += eyeballSpeed
            elif eyeball.radius >= 4 or eyeball.radius <= -2:
                eyeBallMoveable = False

#Detect leap motion roll (hand rotation about x)
def detectHandRoll():
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    roll = math.degrees(hand.palm_normal.roll)
    return roll
#Detect leap motion yaw (hand rotation about y)
def detectHandPitch():
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    pitch= math.degrees(hand.palm_normal.pitch)
    return pitch
c = Leap.Controller()


#Ending text

T2 = text(text='Good work!',
                  align='center', color=color.green, pos=(0, 4, 0), visible =
          False)
T3 = text(text='You failed!',
                  align='center', color=color.green, pos=(0, 4, 0), visible =
          False)

T2.visible = False
T3.visible = False


#To get rid of the stye, user must rotate eyeball with their hands to a
# viewable position then click on it
def process():
    print('processing')
    ev = scene.mouse.getclick()

    print('clicked at' + str(ev.pos[0]))
    print(e.pos[0])
    sphere(pos=ev.pos, radius=0.1, visible = False)
    if abs(ev.pos[0] - e.pos[0]) < 0.25:
        print('collide')
        e.visible = False
        T2.visible = True
        T.visible = False
        T3.visible = False
    else:
        T3.visible = True
        T.visible = False
        T2.visible = False

x = 0
y = 0
z = 0

#Loop acts as timerfired:  when pitch/roll detected change eyeball position
# to simulate rotation.
while T3.visible == False and T2.visible == False:
    f = c.frame()

    zoom()
    pitch = detectHandPitch() +90
    roll = detectHandRoll()
    if roll < -50:
        pitch = 0
        rate(abs(roll) /2 * 50)  # Sets Animation Speed
        ang = 0.005
        x,y,z = 0,1,0
        eyeball.pos[0] +=0.0025

    if roll>50:
        pitch = 0
        rate(abs(roll) / 2 * 50)
        x, y, z = 0, 1, 0
        ang = -0.005
        eyeball.pos[0] -= 0.0025


    if pitch < -50:
        roll = 0
        rate(abs(pitch)/2*50)
        ang = -0.005
        x,y,z = 1,0,0
    if pitch >50:
        roll = 0
        rate(abs(pitch)/2 * 50)
        ang = 0.005
        x, y, z = 1, 0, 0



    eyeball.rotate(eyeball.pos, angle=ang,axis=(x,y,z))
    v = rotate(v,angle=ang,  axis=(x,y,z))
    e.pos = eyeball.pos + v

    # e.rotate(angle = ang, axis = (x,y,z))
    scene.bind('keydown', process)
