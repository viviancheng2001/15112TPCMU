import Leap, sys, thread, time
import sys
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")
from Leap.Other import Leap
from Leap.Other.Leap import SwipeGesture
from Tkinter import *
from PIL import Image, ImageTk


from visual import *

scene.range = 5 #Sets Zoom Distance
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

eyeBoard[random.randint(0,len(eyeBoard)-1)][random.randint(0,len(eyeBoard)-1)]\
    = 250

tex = materials.texture(data=eyeBoard,
                     mapping="sign",
                     interpolate=True)

#mybox = box(pos=(1,1,1,), length=2, height=3, width=2)

eyeball= sphere(material =tex, radius = 1)
# earthlabel = label(pos=eyeball.pos,
#     text='Earth', xoffset=20,
#     yoffset=12, space=eyeball.radius,
#     height=10, border=6,
#     font='sans')

T = text(text='Fix the eye',
     align='center',pos = (0,1,0), color=color.green)

def zoom():
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    hand_speed = hand.palm_velocity
    #print(hand_speed[1])
    if hand_speed[1] <-50 and eyeball.radius >-4:
        eyeball.radius -=abs(hand_speed[1]) / 50000
    elif hand_speed[1] > 50 and eyeball.radius < 4:
        eyeball.radius +=abs(hand_speed[1]) / 50000
        print(eyeball.radius)


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


x = 0
y = 0
z = 0
while True:  # Endless Loop
    f = c.frame()
    # if zoom() == True:
    #     if eyeball.radius + 0.01<5:
    #         eyeball.radius+=0.001
    if not f.hands.is_empty:
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
        elif roll>50:
            pitch = 0
            rate(abs(roll) / 2 * 50)
            x, y, z = 0, 1, 0
            ang = -0.005
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

        eyeball.rotate(angle=ang, axis=(x,y,z))

