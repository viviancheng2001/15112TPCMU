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

#Implements functions from leapMotion database to obtain hand data
###############################################################################

from visual import *


scene.range = 5 #Sets Zoom Distance
scene.width = 500
scene.height = 500
scene.autocenter = True #Auto Centers Camera on Scene
ang = 0.005
eyeBoard=       [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1],
                 [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                 [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                 [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1],
                 [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

# eyeBoard[random.randint(0,len(eyeBoard)-1)][random.randint(0,len(eyeBoard)-1)]\
#     = 250

# tex = materials.texture(data=eyeBoard,
#                      mapping="sign",
#                      interpolate=False)

im = Image.open('images/eyeNew.jpg')  # size must be power of 2, ie 128 x 128
tex = materials.texture(data=im, mapping='sign')




eyeball= sphere(pos = [0,0,0], material =tex, radius = 1)
v= vector(eyeball.radius,0,0)
e = sphere(color=
           color.red, pos=eyeball.pos + v, radius= \
               0.2)


eyeballSpeed = 0


# Velocity v of the Moon (m/s)
wM = abs(eyeballSpeed)/(e.radius)
wE = abs(eyeballSpeed)/eyeball.radius

theta0 = 0
def positionEyeball(t):
    theta = theta0 + wM * t
    return theta

def positione(t):
    theta = theta0 + wE * t
    return theta

t = 0
thetaTerra1 = 0
dt = 5000
dthetaE = positionEyeball(t+dt)- positionEyeball(t)
dthetae = positione(t+dt) - positione(t)





T = text(text='Fix the eye',
     align='center',pos = (0,1,0), color=color.green,linecolor = color.red)

def zoom(eyeBallMoveable = True):
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    hand_speed = hand.palm_velocity
    #print(hand_speed[1])
    if eyeBallMoveable == True:
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

    # evt = scene.waitfor('click keydown')
    # if evt.event == 'click':
    #     print('You clicked at', evt.pos)

def detectHandRoll():
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    roll = math.degrees(hand.palm_normal.roll)
    return roll

def detectHandPitch():
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    pitch= math.degrees(hand.palm_normal.pitch)
    return pitch
c = Leap.Controller()

b = box(pos=(0,0,5), size=(0.5,0.5,0),axis=(1,0,0), color=color.red, opacity =
0.2, makeTrail = True)


def process(ev, i =0.005):
    if ev.key == 'down':
        b.color = color.yellow
        b.pos[1] -= i
    elif ev.key == "up":
        b.color = color.green
        b.pos[1] += i
    elif ev.key == "left":
        b.color = color.blue
        b.pos[0] -=i
    elif ev.key == "right":
        b.color = color.orange
        b.pos[0] +=i

def change(ev):
    e.visible = not e.visible
    if e.visible == False:
        print("SUCCESS!")
x = 0
y = 0
z = 0
while True:  # Endless Loop



    f = c.frame()
    # if zoom() == True:
    #     if eyeball.radius + 0.01<5:
    #         eyeball.radius+=0.001
    if f.hands.is_empty:
        pass
    else:
        scene.bind('click', change)

        # scene.bind('keydown', process)
        zoom()
        pitch = detectHandPitch() +90
        roll = detectHandRoll()
        # print('pitch', pitch)
        # print('roll', roll)
        if roll < -50:
            pitch = 0
            rate(abs(roll) /2 * 50)  # Sets Animation Speed
            ang = 0.005
            x,y,z = 0,1,0
            eyeball.pos[0] +=0.0025
            e.pos[0] += 0.00025

        elif roll>50:
            pitch = 0
            rate(abs(roll) / 2 * 50)
            x, y, z = 0, 1, 0
            ang = -0.005
            eyeball.pos[0] -= 0.0025
            e.pos[0]-=0.00025


        if pitch < -50:
            roll = 0
            rate(abs(pitch)/2*50)
            ang = -0.005
            x,y,z = 1,0,0
        elif pitch >50:
            roll = 0
            rate(abs(pitch)/2 * 50)
            ang = 0.005
            x, y, z = 1, 0, 0

        thetaEyeball = positionEyeball(t + dt) - positionEyeball(t)
        thetae = positione(t + dt) - positione(t)

        eyeball.rotate(eyeball.pos, angle=ang,axis=(x,y,z))
        v = rotate(v,angle=ang,  axis=(x,y,z))
        e.pos = eyeball.pos + v
        t += dt
        # e.rotate(angle = ang, axis = (x,y,z))

