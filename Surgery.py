###############################################################################

# CITATION: Created using outline of provided starterFile leapMotionDemo.py

###############################################################################
import math
# import Leap, sys, thread, time
import sys
import os
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")

from Leap.Other import Leap

from Tkinter import *
from PIL import Image, ImageTk

twistYawPoints = []

twistRollPoints = []
axisPoints = []
def returnPoints():
    return twistYawPoints, twistRollPoints, axisPoints


def init(data):
    data.fX1, data.fY1 = 0,0
    data.fX2, data.fY2 = 0,0
    data.forcepsCollided = False
    data.degrees = 0
    data.app_xR, data.app_yR = 0,0
    data.seen = 0
    data.forcepsX = data.width/2 + 200
    data.forcepsY = data.height/2
    data.objectPlaced = False
    data.size = None
    data.objectBool = False
    data.object = [[None,None] for i in range(random.randint(1,5))]
    data.surgSquarePoints = [[data.width/2 - 200, data.height/2 - 175],
                             [data.width/2 -200, data.height/2 + 175],
                             [data.width/2 +200, data.height/2 + 175],
                             [data.width/2 + 200, data.height/2 -175] ]
    data.leftCut, data.rightCut = 4,4
    data.surg = [data.width / 2 - data.leftCut, data.height / 2 - 150,
                       data.width / 2 + data.rightCut,
                       data.height / 2 + 150]

    data.surgRH = [data.width / 2 + 200, data.height / 2]
    data.surgLH = [data.width / 2 - 200, data.height / 2]
    data.surgInstruction = "Rotate hands outwards to open up wound."
    data.anesthesiaImage = "images/thumbsup.gif"
    data.anesthesiaInstruction = "Grasp syringe handle with hand in position " \
                                 "below"
    data.sutureInstruction = "Aim suture needle tip to green dot"
    data.sutureRightHand = [data.width/1.5, 200]
    data.sutureLeftHand = [220, data.height-200]
    data.sutureLines = []
    data.finishedSuturing = False
    data.suturingBackground = 'images/wound.gif'
    data.suturePointIndex = 0
    data.suturePoints = [[data.width / 2 + 20, data.height / 3 + (
                i * 50)] for i in range(5)]
    print(data.suturePoints)
    data.needle = [data.width/2, data.height - 200]

    data.nextStep = False

    data.dottedLine = [data.width / 2 - 10, data.height / 3.75,
                       data.width / 2 + 10,
                       data.height / 1.5]
    data.hand = [data.width/4, data.height/4, 'images/gloveright.gif']
    data.app_x = None
    data.app_y = None
    data.thumb = False
    data.preCutText = "Zoom in to begin"
    data.currentBottle = 'images/BOTTLE1.gif'
    data.thumbPressed = True #pressing on syringe
    data.canDraw = False
    data.liquidHeight = data.height / 2 + 40
    data.syringe = [data.width/2 - 100, data.height/1.2, 'images/syringe.gif']
    data.hasFailed = False
    data.end = False
    data.thumbPressReminder = False
    data.timer1 = 0
    data.successSyringe = False
    data.seconds = 10
    data.isGrabbing = False
    data.currImage = 'images/surgeryPatient.gif'
    data.controller = Leap.Controller()
    data.mode = "launch"
    data.scissors = ['Scissors', 'images/scissors.gif', data.width - 200,
                     data.height - 175]

    data.cut = False  # whether user has started making incision
    data.lineLst = []


# ****************************************************************

# Each mode represents one step further into the surgical procedure
def mousePressed(event, data):
    if data.mode == "launch":
        launchMousePressed(event,data)
    elif (data.mode == "dental"):
        dentalMousePressed(event, data)
    elif (data.mode == "precut"):
        precutMousePressed(event, data)
    elif (data.mode == "cut"):
        cutMousePressed(event, data)
    elif (data.mode == "stitch"):
        stitchMousePressed(event, data)
    elif (data.mode == "preanesthesia"):
        preanesthesiaMousePressed(event, data)
    elif (data.mode == "anesthesia"):
        anesthesiaMousePressed(event, data)


# This function controls keyPressed for each mode
def keyPressed(event, data):
    if data.mode == "launch":
        launchKeyPressed(event,data)
    elif (data.mode == "dental"):
        dentalKeyPressed(event, data)
    elif (data.mode == "precut"):
        precutKeyPressed(event, data)
    elif (data.mode == "cut"):
        cutKeyPressed(event, data)
    elif (data.mode == "stitch"):
        stitchKeyPressed(event, data)
    elif (data.mode == "preanesthesia"):
        preanesthesiaKeyPressed(event, data)
    elif (data.mode == "anesthesia"):
        anesthesiaKeyPressed(event, data)


# This function controls timerFired for each mode
def timerFired(data):
    if data.mode == "launch":
        launchTimerFired(data)
    elif (data.mode == "dental"):
        dentalTimerFired(data)
    elif (data.mode == "precut"):
        precutTimerFired(data)
    elif (data.mode == "cut"):
        cutTimerFired(data)
    elif (data.mode == "stitch"):
        stitchTimerFired(data)
    elif (data.mode == "preanesthesia"):
        preanesthesiaTimerFired(data)
    elif (data.mode == "anesthesia"):
        anesthesiaTimerFired( data)


# This function controls redrawAll for each mode
def redrawAll(canvas, data):
    if data.mode == "launch":
        launchRedrawAll(canvas,data)
    elif (data.mode == 'dental'):
        dentalRedrawAll(canvas,data)
    elif (data.mode == "precut"):
        precutRedrawAll(canvas, data)
    elif (data.mode == "cut"):
        cutRedrawAll(canvas, data)
    elif (data.mode == "stitch"):
        stitchRedrawAll(canvas, data)
    elif (data.mode == "preanesthesia"):
        preanesthesiaRedrawAll(canvas, data)
    elif (data.mode == "anesthesia"):
        anesthesiaRedrawAll(canvas, data)

####################################
# Launch Screen mode
####################################
# mousePressed not used
def launchMousePressed(event, data):
    if event.x >= data.width/2 + 50 and event.x < data.width/2 + 175 and \
            event.y < data.height/2 + 100 and event.y >= data.height/2 + 50:
        data.currImage = 'images/office.jpg'
        data.mode = "anesthesia"

    elif event.x >= data.width/2 - 175 and event.x < data.width/2 - 50 and \
            event.y >= data.height / 2 + 50 and event.y < data.height/2 + 100:
        print("dental")
        os.system('python Dental.py')



# If key "p" pressed, start game
def launchKeyPressed(event, data):
    pass


# Image starts to bounce around screen
def launchTimerFired(data):
    launchUpdateLeapMotionData(data)
    launchPrintLeapMotionData(data)

def launchUpdateLeapMotionData(data):
    pass


def launchPrintLeapMotionData(data):
    pass

#CITATION: StackOverflow, https://stackoverflow.com/questions/44099594/how-to
# -make-a-tkinter-canvas-rectangle-with-rounded-corners?rq=1
def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):
    points = (
        x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2,
        y1 + r, x2, y2 - r, x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r,
        y2,
        x1 + r, y2, x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1,
        y1)
    return canvas.create_polygon(points, smooth=True, **kwargs)

def launchRedrawAll(canvas,data):
    bg = Image.open('images/opRoom3.jpg')
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!
    text = canvas.create_text(data.width/2, data.height/2 , font = "Arial "
                                                                      "70 "
                                                                 "bold",
                       text = "OPERATE", fill = 'white')

    bbox = canvas.bbox(text)
    rect_item = canvas.create_rectangle(bbox, outline="black", fill="navy")
    canvas.tag_raise(text, rect_item)

    drawDentalButton(canvas,data)
    drawSurgeryButton(canvas,data)
def drawDentalButton(canvas,data):
    round_rectangle(canvas, data.width / 2 - 175, data.height / 2 + 50,
                   data.width / 2 - 50,
                   data.height / 2 + 100,
                   fill=
                   "white")
    canvas.create_text(data.width/2 - 110, data.height/2 + 75,font =
    "Arial 20 bold", fill =
    'black', text = "DENTIST")
def drawSurgeryButton(canvas,data):
    round_rectangle(canvas, data.width / 2 + 50, data.height / 2 + 50,
                    data.width / 2 + 175,
                    data.height / 2 + 100,
                    fill=
                    "black")
    canvas.create_text(data.width / 2 + 110, data.height / 2 + 75, font =
    "Arial 20  bold", fill=
    'white', text="SURGEON")

####################################
# Dental mode
####################################
# mousePressed not used
def dentalMousePressed(event, data):
    pass


# If key "p" pressed, start game
def dentalKeyPressed(event, data):
    pass


# Image starts to bounce around screen
def dentalTimerFired(data):
    dentalUpdateLeapMotionData(data)
    dentalPrintLeapMotionData(data)

def dentalUpdateLeapMotionData(data):
    pass


def dentalPrintLeapMotionData(data):
    pass
def dentalRedrawAll(canvas,data):
    pass

####################################
# precutScreen mode
####################################
# mousePressed not used
def precutMousePressed(event, data):
    pass


# If key "p" pressed, start game
def precutKeyPressed(event, data):
    pass


# Image starts to bounce around screen
def precutTimerFired(data):
    precutUpdateLeapMotionData(data)
    precutPrintLeapMotionData(data)


def checkPinchZoom(data, thumb, index):


    tipThumb = thumb.direction
    tipIndex = index.direction
    indexSpeed = index.tip_velocity
    thumbSpeed = thumb.tip_velocity
    print(math.sqrt((indexSpeed[2]) ** 2))
    print(math.sqrt((thumbSpeed[2]) ** 2))
    print('deg', math.degrees(tipThumb.angle_to(tipIndex)))

    return math.degrees(tipThumb.angle_to(tipIndex)) > 30 and \
            math.sqrt((indexSpeed[2] ** 2)) > 100 and \
            math.sqrt((thumbSpeed[2] ** 2)) > 50
# From the precut screen, user can begin surgical procedure by zooming in on
# the patient's wounds through a "pinch" effect detected by leap motion
def precutUpdateLeapMotionData(data):
    data.frame = data.controller.frame()
    hands = data.frame.hands
    if hands:
        Hand = None
        for item in hands:
            Hand = item
        if Hand:
            fingers = Hand.fingers
            # detect if number of extended fingers is 2
            extended_fingers = len(fingers.extended())
            thumb = fingers.finger_type(0)[0]
            index = fingers.finger_type(1)[0]
            if extended_fingers == 2:
                # to pinch zoom, only index and thumb can be extended
                if fingers.finger_type(2)[0] not in fingers.extended() and \
                        fingers.finger_type(3)[
                            0] not in fingers.extended() and \
                        fingers.finger_type(4)[0] not in fingers.extended():
                    print("THUMBINDEX")
                    # direction of thumb and index when pinch zooming should
                    # be the same
                    if checkPinchZoom(data, thumb, index) == True:
                        print('pinch zoom')
                        data.currImage = 'images/zoomSurgery.gif'
                        # switch to next mode: 1st step of surgery
                        data.mode = "cut"




def precutPrintLeapMotionData(data):
    pass


# Draw out initial view of patient
def precutRedrawAll(canvas, data):


    bg = Image.open(data.currImage)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!
    canvas.create_text(data.width - 200, data.height / 2 - 250,
                       font="Arial 25 bold", text="BEGIN SURGERY")

    canvas.create_text(data.width - 200, data.height / 2 - 200,
                       font="Arial 35 bold", text=data.preCutText)




####################################
# Pre-Anesthesia
####################################
# mousePressed not used
def preanesthesiaMousePressed(event, data):
    pass


# If key "p" pressed, start game
def preanesthesiaKeyPressed(event, data):
    pass


def preanesthesiaTimerFired(data):
    preanesthesiaUpdateLeapMotionData(data)
    preanesthesiaPrintLeapMotionData(data)
    detectTwist(data)


# From the precut screen, user can begin surgical procedure by zooming in on
# the patient's wounds through a "pinch" effect detected by leap motion
def preanesthesiaUpdateLeapMotionData(data):
    frame = data.controller.frame()
    rightHand = frame.hands.rightmost
    leftHand = frame.hands.leftmost

    left_pointable = leftHand.pointables.frontmost
    right_pointable = rightHand.pointables.frontmost

    app_width = 700
    app_height = 600
    # position
    if right_pointable.is_valid or left_pointable.is_valid:
        iBox = frame.interaction_box  # create 2D interaction box with
        leapPointR = right_pointable.stabilized_tip_position
        leapPointL = left_pointable.stabilized_tip_position
        normalizedPointR = iBox.normalize_point(leapPointR, True)
        normalizedPointL = iBox.normalize_point(leapPointL, True)
        app_xL = normalizedPointL.x * app_width
        app_yL = (1 - normalizedPointL.y) * app_height
        app_xR = normalizedPointR.x * app_width
        app_yR = (1 - normalizedPointR.y) * app_height


        data.surgRH[0],data.surgRH[1]  = app_xR,app_yR
        data.app_xR, data.app_yR = app_xR, app_yR
        data.surgLH[0],data.surgLH[1] = app_xL,app_yL


def detectTwist(data):
    axisPoint = 1
    c = data.controller

    # frame1 = c.frame(1)
    # print("prev frame", frame1)
    framePrev = c.frame(1)
    frameCurr = c.frame(0)


    for hand in frameCurr.hands:
        if hand.is_valid:
            roll = math.degrees(hand.palm_normal.roll)
            # print("roll deg:", roll)
            if hand.is_right:
                if roll < - 90 and data.surg[2] < data.width/2 +50:
                    data.surgInstruction = "Keep going!"
                    # print('rollRight')
                    data.surg[2]+=10
            elif hand.is_left:
                if roll > 90 and data.surg[0] > data.width/2  -50:
                    data.surgInstruction = "Keep going!"
                    # print('rollLeft')
                    data.surg[0] -=10

            pitch= math.degrees(hand.direction.pitch)
            print('pitch deg:', pitch)
            if abs(pitch) > 50:
                if pitch<0: #forwards, top decreases
                  for i in range(int(abs(pitch))):
                    if data.surgSquarePoints[0][0] < data.width/2 - 100 and \
                            data.surgSquarePoints[3][0] > data.width/2 + 100:
                        data.surgSquarePoints[0][0] +=0.01
                        data.surgSquarePoints[3][0] -=0.01
                        data.surgSquarePoints[1][0] -= 0.01
                        data.surgSquarePoints[2][0] += 0.01

                        data.surg[1] += 0.005
                else: #backwards, bottom decreases
                  for i in range(int(abs(pitch))):
                      if data.surgSquarePoints[1][0] < data.width/2 - 100 and \
                              data.surgSquarePoints[2][0] > data.width/2 + 100:
                        (data.surgSquarePoints[1])[0] +=0.01
                        (data.surgSquarePoints[2])[0] -=0.01
                        data.surgSquarePoints[0][0] -= 0.01
                        data.surgSquarePoints[3][0] += 0.01
                        data.surg[1] -= 0.005
                        print(data.surg[1])
    if data.seen == 0:
        if data.surg[2] >= data.width/2 + 30 and data.surg[0] <= data.width/2\
                - 30:
            data.surgInstruction = "Wound opened!"
            data.objectBool = True
            data.size = random.randint(15,30)
            placeObject(data)
            data.objectPlaced = True
            data.seen+=1
    if data.objectPlaced == True:
        data.surgInstruction = "Use your index and thumb finger as forceps to remove object."
        data.surgRH[0], data.surgRH[1] = 0,0
        data.surgLH[0], data.surgLH[1] = 0,0
        data.forcepsX = data.app_xR
        data.forcepsY = data.app_yR
        moveForceps(data)
        for i in range(len(data.object)):
            if checkCollisionForceps(data) == True:
                print("COLLLISISISISSIOSOSNONSSONSNSOSNOSNSONSOSNOSNSON")

                data.object.remove(data.object[i])
            else:
                pass

    if len(data.object) == 0:
        data.surgInstruction = "Great job!"
        data.mode = 'stitch'

def checkCollisionForceps(data):
    for i in range(len(data.object)):
        return data.object[i][0] - data.size < data.forcepsX and data.object[i][0] + \
               data.size\
               > data.forcepsX \
               - 150 and data.object[i][1] + data.size <= data.forcepsY and \
               data.object[i][1] - data.size >= (
            data.forcepsY + data.fY2)/2

# canvas.create_rectangle(data.forcepsX,data.forcepsY,data.fX2,
#                        data.fY2, fill = 'pink')


#
# i = 9
#     r = 150
#     angle1 = math.pi / 2 - 2 * math.pi * i / 12
#     data.fX1 = data.forcepsX + r * math.cos(angle1)
#     data.fY1= data.forcepsY - r * math.sin(angle1)
#     canvas.create_line(data.fX1,data.fY1,data.forcepsX,data.forcepsY,
#                        fill="seashell3",
#                        width=10)
#
#     angle2= math.radians(data.degrees)
#     data.fX2= data.forcepsX -r * math.cos(angle2)
#     data.fY2 = data.forcepsY - r * math.sin(angle2)
#     canvas.create_line(data.forcepsX, data.forcepsY, data.fX2,data.fY2,
#                        fill="seashell3", width=10)
#     canvas.create_oval(data.forcepsX - 5, data.forcepsY-5, data.forcepsY + 5,
#                        data.forcepsY + 5, fill = 'pink')
#



import random

def moveForceps(data):
    frame = data.controller.frame()  # controller is a Leap.Controller object
    hands = frame.hands
    right = hands[0]
    if right.is_valid:
        fingers = right.fingers
        thumb = fingers.finger_type(0)[0]
        index = fingers.finger_type(1)[0]
        if thumb.is_valid and index.is_valid:
            dirThumb = thumb.direction
            dirIndex = index.direction
            if thumb in frame.fingers.extended() and index in frame.fingers.extended():
                print("forceps!")
                data.degrees = math.degrees(dirThumb.angle_to(dirIndex))
                print('degrees', data.degrees)
            if dirThumb.distance_to(dirIndex) < 0.2:
                data.degrees = 0




def placeObject(data):
    for i in range(len(data.object)):
        data.object[i][1] = random.randint(int(data.surg[1] + 25),
                                         int(data.surg[3]
                                    -25))
        data.object[i][0] = random.randint(int(data.surg[0] + 25),
                                           int(data.surg[2]
                                    - 25))





            # palm1Position = hand.palm_position
            # direction1 = hand.direction
            #
            # yaw = math.degrees(hand.direction.yaw)
            # roll = math.degrees(hand.palm_normal.roll)
            # twistYawPoints.append(yaw)
            # axisPoints.append(axisPoint)
            # twistRollPoints.append(roll)
            # axisPoint +=1
        # print('roll:', roll)
        # print('yaw:', yaw)

    # new_vector = Leap.Vector()
    # # axis_of_hand_rotation = hand.rotation_axis(frame1)
    # # print(axis_of_hand_rotation)
    # # print(axis_of_hand_rotation)
    # rotation_around_y_axis = hand.rotation_angle(frame1, new_vector.y_axis)
    # rotation_around_x_axis = hand.rotation_angle(frame1, new_vector.x_axis)
    # rotation_around_z_axis = hand.rotation_angle(frame1, new_vector.z_axis)
    # print('x', rotation_around_x_axis)
    # print('y', rotation_around_y_axis)
    # print('z', rotation_around_z_axis)


        # rotation_around_x_axis = hand.rotation_angle(frame1)
        # print('rotation:', rotation_around_x_axis)


def preanesthesiaPrintLeapMotionData(data):
    pass


def drawHands(canvas, data):
    lh = Image.open('images/surgLH.gif')
    # resize to fit canvas
    lh0 = lh.resize((200, 350), Image.ANTIALIAS)
    lh1 = ImageTk.PhotoImage(lh0)

    canvas.create_image(data.surgLH[0], data.surgLH[1], image=lh1)
    label = Label(image=lh1)
    label.image = lh1  # keep a reference!

    rh = Image.open('images/surgRH.gif')
    # resize to fit canvas
    rh0 = rh.resize((200, 350), Image.ANTIALIAS)
    rh1 = ImageTk.PhotoImage(rh0)
    canvas.create_image(data.surgRH[0], data.surgRH[1], image=rh1)
    label = Label(image=rh1)
    label.image = rh1  # keep a reference!

# Draw out initial view of patient
def preanesthesiaRedrawAll(canvas, data):
    canvas.create_rectangle(data.width/2- 350, data.height/2 - 300,
                            data.width/2 + 350, data.height/2+300, fill =
                            'medium sea green')

    canvas.create_polygon(data.surgSquarePoints, fill =
                            'khaki')

    canvas.create_oval(data.surg[0], data.surg[1], data.surg[2], data.surg[3],
        fill = \
        'firebrick',
                           outline = '')

    canvas.create_text(data.width/2, 50, font = "Arial 30 bold", text = \
        data.surgInstruction)

    for j in range(len(data.object)):
        if data.object[j][0] != None and data.object[j][1] != None and \
            data.objectBool == True:

                canvas.create_oval(data.object[j][0]  - data.size, data.object[j][1] -
                                   data.size,
                                   data.object[j][0] + data.size,data.object[j][1]  +
                                   data.size,
                                   fill = 'gray')


    drawHands(canvas, data)
    if data.objectPlaced == True:
        drawForceps(canvas,data)


def drawForceps(canvas,data):
    i = 9
    r = 150
    angle1 = math.pi / 2 - 2 * math.pi * i / 12
    data.fX1 = data.forcepsX + r * math.cos(angle1)
    data.fY1= data.forcepsY - r * math.sin(angle1)
    canvas.create_line(data.fX1,data.fY1,data.forcepsX,data.forcepsY,
                       fill="seashell3",
                       width=10)



    angle2= math.radians(data.degrees)
    data.fX2= data.forcepsX -r * math.cos(angle2)
    data.fY2 = data.forcepsY - r * math.sin(angle2)
    canvas.create_line(data.forcepsX, data.forcepsY, data.fX2,data.fY2,
                       fill="seashell3", width=12)
    # canvas.create_rectangle(data.forcepsX,data.forcepsY,data.fX2,
    #                    data.fY2, fill = 'pink')
    canvas.create_oval(data.forcepsX-5,data.forcepsY-5,data.forcepsX+5,
                       data.forcepsY+5, fill = 'white')
    canvas.create_oval(data.fX2 - 5, data.fY2- 5, data.fX2 + 5,
                       data.fY2 + 5, fill='yellow')
    canvas.create_oval(data.fY1 - 5, data.forcepsY-5, data.fY1+5,
                       data.forcepsY + 5, fill = 'green')
    # canvas.create_rectangle(data.forcepsX, data.forcepsY, data.fX2, data.fY2,
    #                    fill = 'purple')


####################################
# Zeroth step: Anesthesia
####################################
# mousePressed not used
def anesthesiaMousePressed(event, data):
    pass


# If key "p" pressed, start game
def anesthesiaKeyPressed(event, data):
    pass


# Image starts to bounce around screen
def anesthesiaTimerFired(data):
    anesthesiaUpdateLeapMotionData(data)
    anesthesiaPrintLeapMotionData(data)
    checkCollisionSyringeBottle(data)


# From the precut screen, user can begin surgical procedure by zooming in on
# the patient's wounds through a "pinch" effect detected by leap motion
def anesthesiaUpdateLeapMotionData(data):

    frame = data.controller.frame()  # controller is a Leap.Controller object
    hands = frame.hands
    right = hands.rightmost
    app_width = 700
    app_height = 600
    iBox = frame.interaction_box  # create 2D interaction box with
    # dimensions data.width, data.height
    # normalize leap Motion coordinates, map out to Canvas coordinates
    #  app_x and app_y

    rightFingers = right.fingers
    thumb = rightFingers.finger_type(0)[0]

    rightPosition = right.palm_position
    normalizedPoint = iBox.normalize_point(rightPosition, True)
    app_x = normalizedPoint.x * app_width
    app_y = (1 - normalizedPoint.y) * app_height
    data.hand[0] = app_x
    data.hand[1] = app_y
    if handCollideSyringe(data) == True:
        print('touched syringe')
        if len(rightFingers.extended()) == 1 and thumb in rightFingers.extended():
            print('thumbs up hoez')
            data.thumb = True
    if data.thumb == True:
            data.hand[2] = 'images/gloverighthold.gif'
            data.syringe[0]  = app_x- 125
            data.syringe[1] = app_y + 50
            data.thumbPressReminder = True
            if checkCollisionSyringeBottle(data) == True:
                data.anesthesiaInstruction = "Press thumb down to fill " \
                                             "syringe."
                data.anesthesiaImage = 'images/thumbPress1.gif'
                if thumbPressDown(data) == True:
                    if data.liquidHeight <= data.height/ 2 + 85:
                        data.liquidHeight += 5
                        if data.liquidHeight > data.height/2 + 85:
                            data.successSyringe = True
                            data.currImage = 'images/surgeryPatient.gif'
                            data.mode = "precut"


def checkCollisionSyringeBottle(data):
    if data.syringe[0] - 70 > data.width / 4 - 20 and data.syringe[0] - 70 < \
            data.width / 4 + 20 and data.syringe[1] + 75 > data.height / 2 + 30 \
            and data.syringe[1] + 75 < data.height / 2 + 90:
        return True
    else:
        return False





def handCollideSyringe(data):
    return data.hand[0] >   data.syringe[0] + 25 and data.hand[0] < \
           data.syringe[
               0] + 100 and data.hand[1] > data.syringe[1] - 100 and data.hand[1] < \
                                                 data.syringe[1] - 25

def thumbPressDown(data):
    frame = data.controller.frame()  # controller is a Leap.Controller object
    hands = frame.hands
    right = hands[0]
    b = Leap.Bone()
    rightFingers = right.fingers
    thumb = rightFingers.finger_type(0)[0]
    distalThumbBone = thumb.bone(b.TYPE_DISTAL)
    interThumbBone = thumb.bone(b.TYPE_INTERMEDIATE)
    if interThumbBone.is_valid and distalThumbBone.is_valid:
        print('distal,inter  thumb bone valid')
        dirInterBone = interThumbBone.direction
        dirDistalBone = distalThumbBone.direction
        angleInterDistal = dirInterBone.angle_to(dirDistalBone)
        print('angle inter distal:', math.degrees(angleInterDistal))
        if math.degrees(angleInterDistal) > 45:
            return True
        else:
            return False

def anesthesiaPrintLeapMotionData(data):
    pass


def drawBackgroundAnesthesia(canvas,data):
    bg = Image.open('images/office.jpg')
    # resize to fit canvas
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!



    # canvas.create_rectangle(data.width-200-80, data.height/2 + 100 - 65,
    #                         data.width-200+80, data.height/2+100+65,
    #                         fill = 'red')

    handIm0 = Image.open(data.anesthesiaImage)
    # resize to fit canvas
    handIm = handIm0.resize((100,80), Image.ANTIALIAS)
    handIm2 = ImageTk.PhotoImage(handIm)
    canvas.create_image(data.width - 180, data.height / 2 + 70, image=handIm2)
    label = Label(image=handIm2)
    label.image = handIm2  # keep a reference!

    canvas.create_text(50, 50, font="Arial 15 bold", fill='black', text=
    'Fill up the syringe with anesthetic gel in the bottle!', anchor='w')



def drawBottle(canvas,data):
    # container
    canvas.create_rectangle(data.width / 4 - 15, data.height / 2 + 30,
                            data.width / 4 + 15, data.height / 2 + 90, fill=
                            'azure2')
    # liquid
    canvas.create_rectangle(data.width / 4 - 20, data.height / 2 + 40,
                            data.width / 4 + 20, data.height / 2 + 90, fill=
                            'white')
    canvas.create_rectangle(data.width / 4 - 20, data.liquidHeight,
                            data.width / 4 + 20, data.height / 2 + 90, fill=
                            'dodgerblue3')


# Draw out initial view of patient
def anesthesiaRedrawAll(canvas, data):

    drawBackgroundAnesthesia(canvas,data)
    canvas.create_text(data.width-200,data.height/2+7.5, fill = 'black',
                           font = 'Arial 15 bold',
                           text = data.anesthesiaInstruction)



    drawBottle(canvas,data)
    drawSyringe(canvas, data)
    drawHand(canvas, data)


    if data.successSyringe == True:
        canvas.create_text(data.width/2, data.height/2, font = "Arial 30 "
                                                               "bold",
                           fill = 'navy', text = 'Succesfully filled '
                                                         'syringe!')

    # canvas.create_oval( data.syringe[0] - 70 - 10, data.syringe[1] +75- 10,
    #                     data.syringe[0] -70+10, data.syringe[1]+75 + 10, fill =
    #                     'orange')
    #
    #
    # canvas.create_rectangle(data.width/4 - 20,data.height/2 + 30, data.width/4 +
    #                         20, data.height/2 + 90, fill = 'green')
    # drawBottle(canvas, data)
    #





def drawHand(canvas,data):
    hand = Image.open(data.hand[2])
    hand1 = hand.resize((200, 150), Image.ANTIALIAS)
    hand2 = ImageTk.PhotoImage(hand1)
    canvas.create_image(data.hand[0], data.hand[1], image=hand2)
    label = Label(image=hand2)
    label.image = hand2  # keep a reference!

def drawSyringe(canvas,data):
    syr = Image.open(data.syringe[2])
    syr2 = syr.resize((200, 200), Image.ANTIALIAS)
    syr3 = ImageTk.PhotoImage(syr2)
    canvas.create_image(data.syringe[0], data.syringe[1], image=syr3)
    label = Label(image=syr3)
    label.image = syr3  # keep a reference!


####################################
# First step of surgical procedure: creating an incision
####################################

def cutMousePressed(event, data):
    pass


def cutKeyPressed(event, data):
    pass


# Keep track of number of seconds left to make incision, because lagging too
# long will cause harm to the patient
def cutTimerFired(data):
    data.timer1 += 1
    cutUpdateLeapMotionData(data)
    cutPrintLeapMotionData(data)
    if data.timer1 % 10 == 0:
        data.seconds -= 1
        if data.seconds == 0:

            if data.cut == False:
                data.preCutText = "Try Again!"
                reinitIncisionMode(data)
            elif data.hasFailed == False:
                data.mode = "preanesthesia"  # If not failed, advance to next
                # level
            else:
                data.preCutText = "Try Again!"
                reinitIncisionMode(data)
def reinitIncisionMode(data):
    print("Try again!")  # Else try again
    data.seconds = 10
    data.hasFailed = False
    data.cut = False
    data.currImage = 'images/surgeryPatient.gif'
    data.lineLst = []
    data.canDraw = False
    data.isGrabbing = False
    data.mode = 'precut'





# Have virtual surgical scissors follow user's hand to precisely follow and
# cut an incision line on the patient's skin
def cutUpdateLeapMotionData(data):
    frame = data.controller.frame()
    app_width = 700
    app_height = 600
    # Most forward pointing finger
    pointable = frame.pointables.frontmost

    # Map out leapMotion coordinates to 2D coordinates corresponding to Canvas
    #  dimensions
    if pointable.is_valid:
        iBox = frame.interaction_box
        leapPoint = pointable.stabilized_tip_position

        normalizedPoint = iBox.normalize_point(leapPoint, True)
        app_x = normalizedPoint.x * app_width
        app_y = (1 - normalizedPoint.y) * app_height

        # print ("X: " + str(app_x) + " Y: " + str(app_y))
        hand = frame.hands.rightmost
        strength = hand.grab_strength
        # Only able to pick up tool if hand in grasp position
        if strength >0.9:
            data.isGrabbing = True
            print("grabbing")
        else:
            data.isGrabbing = False #######
            print('not grabbing')
        # If grasp, user will now be able to hold and move around the scissors
        if data.isGrabbing == True:
            data.canDraw = True
            data.scissors[2] = app_x
            data.scissors[3] = app_y
            data.app_x = app_x
            data.app_y = app_y
            # When the scissors first touch a point in dotted line,
            # start cutting
            checkFirstCut(data)
        else:
            data.canDraw = True######added
            data.scissors[2] = app_x
            data.scissors[3] = app_y
            data.app_x = app_x
            data.app_y = app_y


xold = None
yold = None

def checkFirstCut(data):
    if data.scissors[2] >= data.dottedLine[0] and data.scissors[2] <= \
            data.dottedLine[2] and data.scissors[3] \
            >= data.dottedLine[1] and data.scissors[3] < \
            data.dottedLine[3]:
        data.cut = True



def cutPrintLeapMotionData(data):
    pass

def drawBackground(canvas,data):

    bg = Image.open(data.currImage)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    canvas.create_line(data.dottedLine[0], data.dottedLine[1],
                       data.dottedLine[2], data.dottedLine[3], fill="gray17",
                       width=5, dash=(2,
                                      4))

    # User instructions
    canvas.create_text(data.width / 2, data.height / 2 - 250, font="Arial "
                                                                   "20 bold",
                       text='Step 1: '
                            'Make '
                            'incision '
                            'along line')

    canvas.create_text(data.width / 2, data.height - 50, text="Time Left: " +
                                                              str(data.seconds),
                       font="Arial 20 bold",
                       fill='white')
    # canvas.create_rectangle(170,150,500,470, fill = 'pink')


def cutRedrawAll(canvas, data):
    drawBackground(canvas,data)

    # Draw out dotted line to use as reference for incision
    # User starts to make incision
    if data.cut and data.isGrabbing == True:
        global xold, yold
        if xold is not None and yold is not None:
            if xold <500 and xold > 170 and yold < 470 and yold > 150 and \
                    data.app_x < 500 and data.app_x > 170 and data.app_y < \
                    470 and data.app_y > 150:
            # Linelst stores new and old x/y coordinates of hand/scissors,
            # which allows user to draw a continuous smooth line
                data.lineLst.append((xold, yold, data.app_x, data.app_y))
        xold = data.app_x
        yold = data.app_y
    else:
        xold = data.app_x
        yold = data.app_y
    # Based on coords in data.lineLst, draw out fluid lines to represent the
    # incision
    drawLine(canvas,data)

    # Draw scissors tool
    drawScissors(canvas,data)
def drawLine(canvas,data):
    if data.canDraw == True:
        for elem in data.lineLst:
            canvas.create_line(elem[0], elem[1], elem[2], elem[3], smooth=True,
                               fill='red', width=10)
            # If go out of bounds (not precise enough): user has failed the task
            # and must retry
            print("Drawing line at: ", elem[0], elem[1], elem[2], elem[3])
            print ("Bounds:", data.dottedLine[0] - 100, data.dottedLine[2] + 100,
                   data.dottedLine[2] - 100 , data.dottedLine[3] + 100)

            if elem[0] < data.dottedLine[0] - 50 or elem[2] > data.dottedLine[
                2] \
                    + 50 or elem[1] < data.dottedLine[1] - 50 or elem[3] > \
                    data.dottedLine[3] + 50:
                data.hasFailed = True
                print("Failed!")



def drawScissors(canvas,data):
    scissors = Image.open('images/scissors.gif')
    scissors1 = scissors.resize((150, 180), Image.ANTIALIAS)
    scissors2 = ImageTk.PhotoImage(scissors1)
    canvas.create_image(data.scissors[2], data.scissors[3],
                        image=scissors2)
    label = Label(image=scissors2)
    label.image = scissors2

################################
# stitch mode
####################################


def stitchMousePressed(event, data):
    pass


def stitchKeyPressed(event, data):
    pass


def stitchTimerFired(data):
    stitchUpdateLeapMotionData(data)


def stitchUpdateLeapMotionData(data):
    frame = data.controller.frame()
    rightHand = frame.hands.rightmost
    leftHand = frame.hands.leftmost

    left_pointable =  leftHand.pointables.frontmost
    right_pointable = rightHand.pointables.frontmost

    data.controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    data.controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    for gesture in frame.gestures():
        if gesture.type is Leap.Gesture.TYPE_CIRCLE:
            circle = Leap.CircleGesture(gesture)
            print('circle!!!!')


    app_width = 700
    app_height = 600
    pointable = right_pointable # finger in most "forward"
    # position
    if data.nextStep != True:
        if pointable.is_valid:
            iBox = frame.interaction_box  # create 2D interaction box with
            leapPoint = pointable.stabilized_tip_position
            normalizedPoint = iBox.normalize_point(leapPoint, True)
            app_x = normalizedPoint.x * app_width
            app_y = (1 - normalizedPoint.y) * app_height
            print ("X: " + str(app_x) + " Y: " + str(app_y))

            data.needle[0] = app_x
            data.needle[1] = app_y
            data.sutureRightHand[0], data.sutureRightHand[1] = data.needle[
                                                                0]+250, \
                                                     data.needle[1] -100
            data.sutureLeftHand[1] = data.needle[1] +75

    for i in range(len(data.suturePoints)):
        if data.needle[0] -35 > (data.suturePoints[i])[0] - 3 and data.needle[
            0] -35\
                <= (data.suturePoints[i])[0] +3 and data.needle[1] + 65 \
                <= (data.suturePoints[i])[1] +3 and data.needle[1]  +65\
                > (data.suturePoints[i])[1] -3:
            print("Pierce")
            data.nextStep = True
            if data.nextStep == True:
                data.needle[0] = 35 + (data.suturePoints[i])[0]
                data.needle[1] = -65 + (data.suturePoints[i])[1]
                data.sutureInstruction = "Make circular gesture with left " \
                                         "forceps to knot wire " \

                if detectRotate(data) == True:
                    print("CIRCLE DETECTEDDDDD")
                    data.sutureLines.append([(data.suturePoints[i])[0] - 50,
                                             (data.suturePoints[i])[1],
                                             (data.suturePoints[i])[0],
                                             (data.suturePoints[i])[1]])
                    print('suturelines', len(data.sutureLines))
                    data.nextStep = False
                    data.sutureInstruction = "Aim suture needle tip to green " \
                                             "dot"
        if len(data.sutureLines) >= 5:
            data.finishedSuturing = True
            data.suturingBackground = 'images/finishedSuturing.gif'
            data.nextStep = False




def detectRotate(data):
    frame = data.controller.frame()
    leftHand = frame.hands.leftmost
    rightHand = frame.hands.rightmost

    left_pointable = leftHand.pointables.frontmost
    # for gesture in frame.gestures():
    #     if gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
    #         screen_tap = Leap.ScreenTapGesture(gesture)
    for gesture in frame.gestures():

        if gesture.type is Leap.Gesture.TYPE_CIRCLE:
            if rightHand not in gesture.hands:
                circle = Leap.CircleGesture(gesture)
                return True

#
# def checkNeedleCollision(data):
#     for i in range(len(data.suturePoints)):
#         if data.needle[0] -35 > (data.suturePoints[i])[0] - 3 and data.needle[
#             0] -35\
#                 <= (data.suturePoints[i])[0] +3 and data.needle[1] + 65 \
#                 <= (data.suturePoints[i])[1] +3 and data.needle[1]  +65\
#                 > (data.suturePoints[i])[1] -3:
#             data.needle[0]= 35+(data.suturePoints[i])[0]
#             data.needle[1] =-65+ (data.suturePoints[i])[1]
#             return True

def stitchPrintLeapMotionData(data):
    pass


def stitchRedrawAll(canvas, data):
    bg = Image.open(data.suturingBackground)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    canvas.create_text(data.width/2, 50, font = "Arial 25 bold", text =
                                                data.sutureInstruction)

    if len(data.sutureLines) <5:
        canvas.create_text(data.width / 2, 100, font="Arial 15 bold", text=
        str(5-len(data.sutureLines)) + " left to go!")
    if data.finishedSuturing == True:
        data.sutureInstruction = "WAY TO GO!"
        pass





    drawSutureNeedle(canvas,data)
    drawSuturePoints(canvas,data)

    for j in range(len(data.sutureLines)):
        [x0,y0,x1,y1] = data.sutureLines[j]
        canvas.create_line(x0,y0,x1,y1, fill = 'mediumpurple1', width = 4)

    #LEFTHAND
    rightHand = Image.open('images/sutureHand.gif')
    rightHand1= rightHand.resize((700, 600), Image.ANTIALIAS)
    rightHand2 = ImageTk.PhotoImage(rightHand1)
    canvas.create_image(data.sutureRightHand[0],data.sutureRightHand[1],
                        image=rightHand2)
    label = Label(image=rightHand2)
    label.image = rightHand2  # keep a reference!

    #LEFTHAND
    leftHand = Image.open('images/leftHand.gif')
    leftHand1 = leftHand.resize((520,420), Image.ANTIALIAS)
    leftHand2 = ImageTk.PhotoImage(leftHand1)
    canvas.create_image(data.sutureLeftHand[0], data.sutureLeftHand[1],
                        image=leftHand2)
    label = Label(image=leftHand2)
    label.image = leftHand2  # keep a reference!








def drawSutureNeedle(canvas,data):
    needle = Image.open('images/sutureNeedle.gif')
    needle1 = needle.resize((100,220), Image.ANTIALIAS)
    needle2 = ImageTk.PhotoImage(needle1)
    canvas.create_image(data.needle[0], data.needle[1],
                        image=needle2)
    label = Label(image=needle2)
    label.image = needle2

    # canvas.create_oval(data.needle[0] - 35 -5, data.needle[1] + 65 -5,
    #                    data.needle[0] -35 + 5, data.needle[1] + 65 +5,
    #                    fill = 'mediumpurple1')

def drawSuturePoints(canvas,data):
    print(len(data.suturePoints))
    for i in range(len(data.suturePoints)):
        canvas.create_oval((data.suturePoints[i])[0] - 3,
                           (data.suturePoints[i])[1] -
                           3, (data.suturePoints[0])[0] +3,
                           (data.suturePoints[i])[1] + 3, fill = 'yellow green')







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
    data.timerDelay = 30  # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    timerFiredWrapper(canvas, data)
    # if data.end == False:
    #
    #     canvas.bind("<Motion>", motion)

    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    # and precut the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(700, 600)
