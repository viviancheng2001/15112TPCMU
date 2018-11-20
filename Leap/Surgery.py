#]import Leap, sys, thread, time
import sys

import random
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")

import Leap
from Leap import SwipeGesture

from Tkinter import *

from PIL import Image, ImageTk


def init(data):
    data.app_x = None
    data.app_y = None
    data.hasFailed = False
    data.end = False
    data.timer1 = 0
    data.seconds = 10
    data.traceLine = []
    data.isGrabbing = False
    data.currImage = 'images/surgeryPatient.gif'
    data.controller = Leap.Controller()
    data.mode = "launch"
    data.scissors = ['Scissors','images/scissors.gif', data.width-200,
                   data.height-175]

    data.soTrue = False
    data.lineLst = []



# *****************************************************************************************

def mousePressed(event, data):
    if (data.mode == "launch"):
        launchMousePressed(event, data)
    elif (data.mode == "real"):
        realMousePressed(event, data)
    elif (data.mode == "stitch"):
        stitchMousePressed(event, data)



# This function controls keyPressed for each mode
def keyPressed(event, data):
    if (data.mode == "launch"):
        launchKeyPressed(event, data)
    elif (data.mode == "real"):
        realKeyPressed(event, data)
    elif (data.mode == "stitch"):
        stitchKeyPressed(event, data)



# This function controls timerFired for each mode
def timerFired(data):
    if (data.mode == "launch"):
        launchTimerFired(data)
    elif (data.mode == "real"):
        realTimerFired(data)
    elif (data.mode == "stitch"):
        stitchTimerFired(data)



# This function controls redrawAll for each mode
def redrawAll(canvas, data):
    if (data.mode == "launch"):
        launchRedrawAll(canvas, data)
    elif (data.mode == "real"):
        realRedrawAll(canvas, data)
    elif (data.mode == "stitch"):
        stitchRedrawAll(canvas, data)


####################################
# launchScreen mode
####################################
# mousePressed not used
def launchMousePressed(event, data):
    pass


# If key "p" pressed, start game
def launchKeyPressed(event, data):
    pass


# Image starts to bounce around screen
def launchTimerFired(data):
    launchUpdateLeapMotionData(data)
    launchPrintLeapMotionData(data)
def launchUpdateLeapMotionData(data):
    data.frame = data.controller.frame()
    hands = data.frame.hands
    if hands:
        Hand = None
        for item in hands:
            if item.is_right:
                Hand = item
        if Hand:
            fingers = Hand.fingers
            extended_fingers = len(fingers.extended())
            thumb = fingers.finger_type(0)[0]
            index = fingers.finger_type(1)[0]
            if extended_fingers == 2:
                if fingers.finger_type(2)[0] not in fingers.extended() and \
                        fingers.finger_type(3)[
                            0] not in fingers.extended() and \
                        fingers.finger_type(4)[0] not in fingers.extended():
                    print("two fingers")
                    tipThumb = thumb.direction
                    tipIndex = index.direction
                    if tipThumb.angle_to(tipIndex) == tipIndex.angle_to(
                            tipThumb):
                        print('pinch')
                        data.currImage = 'images/zoomSurgery.gif'
                        data.mode = "real"

def launchPrintLeapMotionData(data):
    pass
    #######SWIPING SETUP##############

def launchRedrawAll(canvas, data):
    data.dottedLine = [data.width/2 - 10, data.height/3.75, data.width/2+10,
                       data.height/1.5]

    bg = Image.open(data.currImage)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!
    canvas.create_text(data.width - 200, data.height / 2 - 200,
                       font = "Arial 35 bold", text="Zoom in "
                                                                    "to begin")



####################################
# real mode
####################################

def realMousePressed(event,data):
    pass



def realKeyPressed(event, data):
    pass

def realTimerFired(data):
    data.timer1+=1
    realUpdateLeapMotionData(data)
    realPrintLeapMotionData(data)
    if data.timer1 % 10 == 0:
        data.seconds -=1
        if data.seconds == 0:
            if data.hasFailed == False:
                data.mode = "stitch"
            else:
                print("Try again!")
                init(data)


def realUpdateLeapMotionData(data):
    frame = data.controller.frame()
    app_width = 700
    app_height = 600
    pointable = frame.pointables.frontmost

    if pointable.is_valid:
        iBox = frame.interaction_box
        leapPoint = pointable.stabilized_tip_position

        normalizedPoint = iBox.normalize_point(leapPoint, True)
        app_x = normalizedPoint.x * app_width
        app_y = (1 - normalizedPoint.y) * app_height

        print ("X: " + str(app_x) + " Y: " + str(app_y))
        hand = frame.hands.rightmost
        strength = hand.grab_strength
        if strength > 0.8:
            data.isGrabbing = True
            print("grabbing")
        if data.isGrabbing == True:
            data.scissors[2] = app_x
            data.scissors[3] = app_y
            data.app_x = app_x
            data.app_y = app_y
            if data.scissors[2] >= data.dottedLine[0] and data.scissors[2] <=\
                    data.dottedLine[2] and data.scissors[3] \
                    >=data.dottedLine[1] and data.scissors[3] < \
                    data.dottedLine[3]:
                data.soTrue = True
xold = None
yold = None


def realPrintLeapMotionData(data):
    pass


def realRedrawAll(canvas, data):
    bg = Image.open(data.currImage)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!
    canvas.create_line(data.dottedLine[0], data.dottedLine[1],
                       data.dottedLine[2],data.dottedLine[3], fill="gray17",
                       width = 5,dash=(2,
                                                                         4))
    canvas.create_text(data.width/2, data.height/2 - 250, font = "Arial "
                                                                 "20 bold",
                       text = 'Step 1: '
                                                                  'Make '
                                                                  'incision '
                                                                  'along line')
    if data.soTrue:
        global xold, yold
        if xold is not None and yold is not None:
            # here's where you draw it. smooth. neat.
            data.lineLst.append((xold, yold, data.app_x, data.app_y))
        xold = data.app_x
        yold = data.app_y
    for elem in data.lineLst:
        canvas.create_line(elem[0], elem[1], elem[2], elem[3], smooth=True,
        fill='red', width=10)
        if elem[0] < data.dottedLine[0] - 100 or elem[2] > data.dottedLine[2] \
                + 100 or elem[1] < data.dottedLine[2] - 100 or elem[3] > \
                data.dottedLine[3] + 100:
            print(elem[0],elem[1],elem[2],elem[3])
            data.hasFailed = True
    scissors = Image.open('images/scissors.gif')
    scissors1= scissors.resize((150,180), Image.ANTIALIAS)
    scissors2 = ImageTk.PhotoImage(scissors1)
    canvas.create_image(data.scissors[2],data.scissors[3],
                        image=scissors2)
    label = Label(image=scissors2)
    label.image = scissors2
    for i in data.traceLine:
        canvas.create_oval(i[0]-10,i[1]-10,i[0]+10,i[1]+10, outline="red",
                                fill="red", width=2, stipple="gray50")
    canvas.create_text(data.width/2, data.height-50,text = "Time Left: " +
                                                           str(data.seconds),
                       font = "Arial 20 bold",
                       fill = 'white')



################################
# stitch mode
####################################


def stitchMousePressed(event,data):
    pass


def stitchKeyPressed(event, data):
    pass

def stitchTimerFired(data):
    pass


def stitchUpdateLeapMotionData(data):
    pass


def stitchPrintLeapMotionData(data):
    pass


def stitchRedrawAll(canvas, data):
    bg = Image.open('images/openWound.gif')
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!







#######################################
# use the run function as-is
####################################
    # if data.end == False:
    #
    #     canvas.bind("<Motion>", motion)

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    timerFiredWrapper(canvas,data)
    # if data.end == False:
    #
    #     canvas.bind("<Motion>", motion)

    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700,600)

