import Leap, sys, thread, time
import sys
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")
from Leap.Other import Leap
from Leap.Other.Leap import SwipeGesture
from Tkinter import *
from PIL import Image, ImageTk


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

# mybox = box(pos=(1,1,1,), length=2, height=3, width=0.1)



eyeball= sphere(pos = [0,0,0], material =tex, radius = 1, axis = (1,0,0))
# L = label( pos=(0,0,0), linecolor = color.red, opacity = 0.1,
#     height=50, text = "    ")



# vect = (eyeball.radius*2,0,0)
vect = [eyeball.radius,0,0]
e = sphere(color =
color.red, pos = eyeball.pos -vect,
           axis = (1, 0,0),radius = \
    0.1)







T = text(text='Fix the eye',
     align='center',pos = (0,1,0), color=color.green,linecolor = color.red)

def zoom(eyeBallMoveable = True):
    frame = Leap.Controller().frame()
    hand = frame.hands[0]
    hand_speed = hand.palm_velocity
    #print(hand_speed[1])
    if eyeBallMoveable == True:
        if hand_speed[1] <-50 and eyeball.radius >-2:
            eyeball.radius -=abs(hand_speed[1]) / 500000
            e.radius -=abs(hand_speed[1]) / 500000
        elif hand_speed[1] > 50 and eyeball.radius < 4:
            eyeball.radius +=abs(hand_speed[1]) / 500000
            e.radius += abs(hand_speed[1]) / 500000
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


def process(ev, i =0.000005):
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
            eyeball.pos[0] +=0.0025
            e.pos[0] +=0.0025
        elif roll>50:
            pitch = 0
            rate(abs(roll) / 2 * 50)
            x, y, z = 0, 1, 0
            ang = -0.005
            eyeball.pos[0] -= 0.0025
            e.pos[0] -= 0.0025
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
        e.rotate(angle = ang, axis = (x,y,z))
        scene.bind('keydown', process)

