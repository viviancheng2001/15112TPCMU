###############################################################################

# CITATION: Created using outline of provided starterFile leapMotionDemo.py

###############################################################################
import math
# import Leap, sys, thread, time
import sys

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
    data.dottedLine = [data.width / 2 - 10, data.height / 3.75,
                       data.width / 2 + 10,
                       data.height / 1.5]
    data.hand = [data.width/4, data.height/4, 'images/gloveright.gif']
    data.app_x = None
    data.app_y = None
    data.thumb = False
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
    data.mode = "preanesthesia"
    data.scissors = ['Scissors', 'images/scissors.gif', data.width - 200,
                     data.height - 175]

    data.cut = False  # whether user has started making incision
    data.lineLst = []


# ****************************************************************

# Each mode represents one step further into the surgical procedure
def mousePressed(event, data):
    if (data.mode == "launch"):
        launchMousePressed(event, data)
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
    if (data.mode == "launch"):
        launchKeyPressed(event, data)
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
    if (data.mode == "launch"):
        launchTimerFired(data)
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
    if (data.mode == "launch"):
        launchRedrawAll(canvas, data)
    elif (data.mode == "cut"):
        cutRedrawAll(canvas, data)
    elif (data.mode == "stitch"):
        stitchRedrawAll(canvas, data)
    elif (data.mode == "preanesthesia"):
        preanesthesiaRedrawAll(canvas, data)
    elif (data.mode == "anesthesia"):
        anesthesiaRedrawAll(canvas, data)


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


# From the launch screen, user can begin surgical procedure by zooming in on
# the patient's wounds through a "pinch" effect detected by leap motion
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
                    # direction of thumb and index when pinch zooming should
                    # be the same
                    tipThumb = thumb.direction
                    tipIndex = index.direction
                    if tipThumb.angle_to(tipIndex) == tipIndex.angle_to(
                            tipThumb):
                        print('pinch zoom')
                        data.currImage = 'images/zoomSurgery.gif'
                        # switch to next mode: 1st step of surgery
                        data.mode = "cut"


def launchPrintLeapMotionData(data):
    pass


# Draw out initial view of patient
def launchRedrawAll(canvas, data):


    bg = Image.open(data.currImage)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!
    canvas.create_text(data.width - 200, data.height / 2 - 200,
                       font="Arial 35 bold", text="Zoom in "
                                                  "to begin")



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


# From the launch screen, user can begin surgical procedure by zooming in on
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


# From the launch screen, user can begin surgical procedure by zooming in on
# the patient's wounds through a "pinch" effect detected by leap motion
def anesthesiaUpdateLeapMotionData(data):

    frame = data.controller.frame()  # controller is a Leap.Controller object
    hands = frame.hands
    left = hands.leftmost
    right = hands.rightmost
    app_width = 700
    app_height = 600

    iBox = frame.interaction_box  # create 2D interaction box with
    # dimensions data.widthxdata.height
    # normalize leap Motion coordinates, map out to Canvas coordinates
    #  app_x and app_y

    b = Leap.Bone()
    rightFingers = right.fingers
    thumb = rightFingers.finger_type(0)[0]
    distalThumbBone = thumb.bone(b.TYPE_DISTAL)
    interThumbBone = thumb.bone(b.TYPE_INTERMEDIATE)





    # detect if number of extended fingers is 2



    rightPosition = right.palm_position
    normalizedPoint = iBox.normalize_point(rightPosition, True)
    app_x = normalizedPoint.x * app_width
    app_y = (1 - normalizedPoint.y) * app_height
    data.hand[0] = app_x
    data.hand[1] = app_y
    if data.hand[0] >   data.syringe[0] + 50 and data.hand[0] < data.syringe[
        0] + 100 and data.hand[1] > data.syringe[1] - 100 and data.hand[1] < \
            data.syringe[1] - 50:
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
                if right.is_right:
                    if interThumbBone.is_valid and distalThumbBone.is_valid:
                        print('distal,inter  thumb bone valid')
                        dirInterBone = interThumbBone.direction
                        dirDistalBone = distalThumbBone.direction
                        angleInterDistal = dirInterBone.angle_to(dirDistalBone)
                        print('angle inter distal:', angleInterDistal)
                        if angleInterDistal > .75:
                            if data.liquidHeight <= data.height/ 2 + 85:
                                data.liquidHeight += 5
                                if data.liquidHeight > data.height/2 + 85:
                                    data.successSyringe = True
                                    data.mode = "launch"


def anesthesiaPrintLeapMotionData(data):
    pass


# Draw out initial view of patient
def anesthesiaRedrawAll(canvas, data):

    if data.thumbPressReminder == True:
        canvas.create_text(data.width-100,data.height/2+5 , fill = 'black',
                           font = 'Arial 15 bold',
                           text = "Aim syringe into bottle and press thumb "
                                  "down ", anchor
                           = 'e')
    bg = Image.open('images/office.jpg')
    # resize to fit canvas
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!
    canvas.create_text(50,50, font = "Arial 15 bold", fill = 'black', text =
    'Fill up the syringe with anesthetic gel in the bottle!', anchor = 'w')

    #container
    canvas.create_rectangle(data.width / 4 - 15, data.height / 2 + 30,
                            data.width / 4 + 15, data.height / 2 + 90, fill=
                            'azure2')
    #liquid
    canvas.create_rectangle(data.width/4 - 20, data.height / 2 + 40,
                            data.width/4 + 20, data.height/2  + 90,fill =
    'white')
    canvas.create_rectangle(data.width / 4 - 20, data.liquidHeight,
                            data.width / 4 + 20, data.height / 2 + 90, fill=
                            'dodgerblue3')



    # bot = Image.open('images/anesbottle.gif')
    # bot2 = bot.resize((150,150), Image.ANTIALIAS)
    # bot3 = ImageTk.PhotoImage(bot2)
    # canvas.create_image(data.width / 4, data.height / 2, image=bot3)
    # label = Label(image=bot3)
    # label.image = bot3  # keep a reference!

    hand = Image.open(data.hand[2])
    hand1 = hand.resize((200, 150), Image.ANTIALIAS)
    hand2 = ImageTk.PhotoImage(hand1)
    canvas.create_image(data.hand[0], data.hand[1], image=hand2)
    label = Label(image=hand2)
    label.image = hand2 # keep a reference!

    syr = Image.open(data.syringe[2])
    syr2 = syr.resize((200, 200), Image.ANTIALIAS)
    syr3 = ImageTk.PhotoImage(syr2)
    canvas.create_image(data.syringe[0], data.syringe[1], image=syr3)
    label = Label(image=syr3)
    label.image = syr3  # keep a reference!
    if data.successSyringe == True:
        canvas.create_text(data.width/2, data.height/2, font = "Arial 30 "
                                                               "bold",
                           fill = 'navy', text = 'Succesfully filled '
                                                         'syringe!')



def checkCollisionSyringeBottle(data):
     if data.syringe[0] - 70 > data.width/4 - 15 and data.syringe[0] <\
             data.width/4 + 15  or  data.syringe[1] + 75 > data.height/2 + 30\
             and data.syringe[1] + 75 < data.height/2 + 90:
         return True
     else:
         return False


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
            if data.hasFailed == False:
                data.mode = "stitch"  # If not failed, advance to next level
            else:
                print("Try again!")  # Else try again
                data.seconds = 10
                data.mode = 'cut'


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
            if data.scissors[2] >= data.dottedLine[0] and data.scissors[2] <= \
                    data.dottedLine[2] and data.scissors[3] \
                    >= data.dottedLine[1] and data.scissors[3] < \
                    data.dottedLine[3]:
                data.cut = True


xold = None
yold = None




def cutPrintLeapMotionData(data):
    pass


def cutRedrawAll(canvas, data):
    bg = Image.open(data.currImage)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    # Draw out dotted line to use as reference for incision
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
    # User starts to make incision
    if data.cut:
        global xold, yold
        if xold is not None and yold is not None:
            # Linelst stores new and old x/y coordinates of hand/scissors,
            # which allows user to draw a continuous smooth line
            data.lineLst.append((xold, yold, data.app_x, data.app_y))
        xold = data.app_x
        yold = data.app_y
    # Based on coords in data.lineLst, draw out fluid lines to represent the
    # incision
    if data.canDraw == True and data.isGrabbing == True:
        for elem in data.lineLst:
            canvas.create_line(elem[0], elem[1], elem[2], elem[3], smooth=True,
                               fill='red', width=10)
            # If go out of bounds (not precise enough): user has failed the task
            # and must retry
            print("Drawing line at: ", elem[0], elem[1], elem[2], elem[3])
            print ("Bounds:", data.dottedLine[0] - 100, data.dottedLine[2] + 100,
                   data.dottedLine[2] - 100 , data.dottedLine[3] + 100)

            if elem[0] < data.dottedLine[0] - 25 or elem[2] > data.dottedLine[2] \
                    + 25 or elem[1] < data.dottedLine[1] - 25 or elem[3] > \
                    data.dottedLine[3] + 25:
                data.hasFailed = True
                print("Failed!")

    # Draw scissors tool
    scissors = Image.open('images/scissors.gif')
    scissors1 = scissors.resize((150, 180), Image.ANTIALIAS)
    scissors2 = ImageTk.PhotoImage(scissors1)
    canvas.create_image(data.scissors[2], data.scissors[3],
                        image=scissors2)
    label = Label(image=scissors2)
    label.image = scissors2

    canvas.create_text(data.width / 2, data.height - 50, text="Time Left: " +
                                                              str(data.seconds),
                       font="Arial 20 bold",
                       fill='white')


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
    bg = Image.open('images/woundenhanced.jpg')
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
    data.timerDelay = 100  # milliseconds
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
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(700, 600)
