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
    data.suturePointIndex = 0
    data.suturePoints = [[data.width / 2 + 20, data.height / 3 + (
                i * 45)] for i in range(5)]
    print(data.suturePoints)
    data.needle = [data.width/2, data.height - 200]



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
    data.mode = "stitch"
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
            if item.is_right:
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
    pass



def detectTwist(data):
    axisPoint = 1
    c = Leap.Controller()

    # frame1 = c.frame(1)
    # print("prev frame", frame1)
    frame2 = c.frame(0)
    fps = frame2.current_frames_per_second
    print('fps',fps)

    print('frame', frame2)

    hand = frame2.hands[0]
    if hand.is_valid:

        palm1Position = hand.palm_position
        direction1 = hand.direction

        yaw = math.degrees(hand.direction.yaw)
        roll = math.degrees(hand.palm_normal.roll)
        twistYawPoints.append(yaw)
        axisPoints.append(axisPoint)
        twistRollPoints.append(roll)
        axisPoint +=1
        print('roll:', roll)
        print('yaw:', yaw)

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



    # if Hand:
        #     fingers = Hand.fingers
        #     if not data.frame.fingers.is_empty:
        #         extended_finger_list = data.frame.fingers.extended()
        #         if len(extended_finger_list) == 5:
        #             print("all extended")
        #             for finger in extended_finger_list:
        #


def preanesthesiaPrintLeapMotionData(data):
    pass


# Draw out initial view of patient
def preanesthesiaRedrawAll(canvas, data):
    table = Image.open('images/table.jpg')
    # resize to fit canvas
    table1 = table.resize((700, 600), Image.ANTIALIAS)
    table2 = ImageTk.PhotoImage(table1)
    canvas.create_image(data.width / 2, data.height / 2, image=table2)
    label = Label(image=table2)
    label.image = table2  # keep a reference!

    bottle = Image.open(data.currentBottle)
    # resize to fit canvas
    bottle2 = bottle.resize((500,500), Image.ANTIALIAS)
    bottle3 = ImageTk.PhotoImage(bottle2)
    canvas.create_image(data.width / 2, data.height / 2, image=bottle3)
    label = Label(image=bottle3)
    label.image = bottle3  # keep a reference!




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
                if thumbPressDown(data) == True:
                        if data.liquidHeight <= data.height/ 2 + 85:
                            data.liquidHeight += 5
                            if data.liquidHeight > data.height/2 + 85:
                                data.successSyringe = True
                                data.currImage = 'images/surgeryPatient.gif'
                                data.mode = "precut"


def checkCollisionSyringeBottle(data):
    if data.syringe[0] - 70 > data.width/4 - 15 and data.syringe[0] <\
            data.width/4 + 15  or  data.syringe[1] + 75 > data.height/2 + 30\
            and data.syringe[1] + 75 < data.height/2 + 90:
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
    right = hands.rightmost
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
        if math.degrees(angleInterDistal) > 60:
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
    if data.thumbPressReminder == True:
        canvas.create_text(data.width-100,data.height/2+5 , fill = 'black',
                           font = 'Arial 15 bold',
                           text = "Aim syringe into bottle and press thumb "
                                  "down ", anchor
                           = 'e')
    drawBottle(canvas,data)
    drawSyringe(canvas,data)
    drawHand(canvas,data)


    if data.successSyringe == True:
        canvas.create_text(data.width/2, data.height/2, font = "Arial 30 "
                                                               "bold",
                           fill = 'navy', text = 'Succesfully filled '
                                                         'syringe!')

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
                data.mode = "stitch"  # If not failed, advance to next level
            else:
                data.preCutText = "Try Again!"
                reinitIncisionMode(data)
def reinitIncisionMode(data):
    print("Try again!")  # Else try again
    data.seconds = 10
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
    pass


def stitchUpdateLeapMotionData(data):
    pass


def stitchPrintLeapMotionData(data):
    pass


def stitchRedrawAll(canvas, data):
    bg = Image.open('images/wound.gif')
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    drawSutureNeedle(canvas,data)
    drawSuturePoints(canvas,data)


def drawSutureNeedle(canvas,data):
    needle = Image.open('images/sutureNeedle.gif')
    needle1 = needle.resize((100,220), Image.ANTIALIAS)
    needle2 = ImageTk.PhotoImage(needle1)
    canvas.create_image(data.needle[0], data.needle[1],
                        image=needle2)
    label = Label(image=needle2)
    label.image = needle2

def drawSuturePoints(canvas,data):
    print(len(data.suturePoints))
    for i in range(len(data.suturePoints)):
        canvas.create_oval((data.suturePoints[i])[0] - 2,
                           (data.suturePoints[i])[1] -
                           2, (data.suturePoints[i])[0] +2,
                           (data.suturePoints[i])[1] + 2, fill = "black")






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
