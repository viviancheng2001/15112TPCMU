###############################################################################

# CITATION: Created using outline of provided starterFile leapMotionDemo.py
# Uses leapMotion built-in variables/gesture-detection functions from leap
# motion library
# Uses 112 Tkinter Framework, from the CMU 15-112 course
###############################################################################
import math
import os
import random
# import Leap, sys, thread, time
import sys
import os
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")
from Leap.Other import Leap
from Tkinter import *
from PIL import Image, ImageTk


def init(data):
    # data.timer = 0
    data.seenFact = 0
    #CITATION: medical facts are from online (
    # https://www.disabled-world.com/medical/human-body-facts.php)
    data.medText = 'medFacts.txt'
    data.medFacts = [line for line in open(data.medText)]
    data.displayFact = False
    data.progressText = ["STEP 1: ANESTHESIA","STEP 2: INCISION", "STEP 3: "
                                                             "EXTRACT",
                         "STEP 4: STITCH"]
    #Initialize mode and controller
    data.mode = "launch" #current mode
    data.controller = Leap.Controller()

    ######Surgery: Anesthesia########
    data.anesthesiaImage = "images/thumbsup.gif"
    data.anesthesiaInstruction = "Grasp syringe handle with hand in position " \
                                 "below"
    data.currentBottle = 'images/BOTTLE1.gif'
    data.thumbPressed = True #pressing on syringe
    data.canDraw = False
    data.liquidHeight = data.height / 2 + 40
    data.syringe = [data.width/2 - 100, data.height/1.2, 'images/syringe.gif']
    data.hasFailed = False
    data.end = False
    data.timer1= 0
    data.thumbPressReminder = False
    data.successSyringe = False
    data.seconds = 10
    data.isGrabbing = False
    data.currImage = 'images/surgeryPatient.gif'

    ######Surgery: Precut#######
    data.preCutText = "Zoom in to begin"
    data.scissors = ['Scissors', 'images/scissors.gif', data.width - 200,
                     data.height - 175]

    data.cut = False  # whether user has started making incision
    data.lineLst = []

    #######Surgery: Cut########
    data.dottedLine = [data.width / 2 - 10, data.height / 3.75,
                       data.width / 2 + 10,
                       data.height / 1.5]
    data.hand = [data.width / 4, data.height / 4, 'images/gloveright.gif']
    data.app_x = None
    data.app_y = None
    data.thumb = False

    #######Surgery: Extraction########
    data.fX1, data.fY1 = 0, 0
    data.fX2, data.fY2 = 0, 0
    data.forcepsCollided = False
    data.degrees = 0
    data.app_xR, data.app_yR = 0, 0
    data.seen = 0
    data.forcepsX = data.width / 2 + 200
    data.forcepsY = data.height / 2
    data.objectPlaced = False
    data.size = None
    data.objectBool = False
    data.object = [[None, None] for i in range(random.randint(1, 5))]
    data.surgSquarePoints = [[data.width / 2 - 200, data.height / 2 - 175],
                             [data.width / 2 - 200, data.height / 2 + 175],
                             [data.width / 2 + 200, data.height / 2 + 175],
                             [data.width / 2 + 200, data.height / 2 - 175]]
    data.leftCut, data.rightCut = 4, 4
    data.surg = [data.width / 2 - data.leftCut, data.height / 2 - 150,
                 data.width / 2 + data.rightCut,
                 data.height / 2 + 150]

    data.surgRH = [data.width / 2 + 200, data.height / 2]
    data.surgLH = [data.width / 2 - 200, data.height / 2]
    data.surgInstruction = "Rotate hands outwards to open up wound."

    #######Surgery: Suture########
    data.sutureInstruction = "Aim suture needle tip to green dot"
    data.sutureRightHand = [data.width / 1.5, 200]
    data.sutureLeftHand = [220, data.height - 200]
    data.sutureLines = []
    data.finishedSuturing = False
    data.suturingBackground = 'images/wound.gif'
    data.suturePointIndex = 0
    data.suturePoints = [[data.width / 2 + 20, data.height / 3 + (
            i * 50)] for i in range(5)]
    data.needle = [data.width / 2, data.height - 200]

    data.nextStep = False


# ****************************************************************
# Each mode represents one step further into the surgical procedure
def mousePressed(event, data):
    if data.mode == "launch":
        launchMousePressed(event,data)
    elif (data.mode == "precut"):
        precutMousePressed(event, data)
    elif (data.mode == "cut"):
        cutMousePressed(event, data)
    elif (data.mode == "stitch"):
        stitchMousePressed(event, data)
    elif (data.mode == "extract"):
        extractionMousePressed(event, data)
    elif (data.mode == "anesthesia"):
        anesthesiaMousePressed(event, data)
    elif (data.mode == "end"):
        endMousePressed(event, data)


# This function controls keyPressed for each mode
def keyPressed(event, data):
    if data.mode == "launch":
        launchKeyPressed(event,data)
    elif (data.mode == "precut"):
        precutKeyPressed(event, data)
    elif (data.mode == "cut"):
        cutKeyPressed(event, data)
    elif (data.mode == "stitch"):
        stitchKeyPressed(event, data)
    elif (data.mode == "extract"):
        extractionKeyPressed(event, data)
    elif (data.mode == "anesthesia"):
        anesthesiaKeyPressed(event, data)
    elif (data.mode == "end"):
        endKeyPressed(event, data)


# This function controls timerFired for each mode
def timerFired(data):
    if data.timer1%100 == 0:
        data.displayFact = True
    else:
        data.displayFact = False
        data.seenFact+=1


    if data.mode == "launch":
        launchTimerFired(data)
    elif (data.mode == "precut"):
        precutTimerFired(data)
    elif (data.mode == "cut"):
        cutTimerFired(data)
    elif (data.mode == "stitch"):
        stitchTimerFired(data)
    elif (data.mode == "extract"):
        extractionTimerFired(data)
    elif (data.mode == "anesthesia"):
        anesthesiaTimerFired( data)
    elif (data.mode == "end"):
        endTimerFired(data)


# This function controls redrawAll for each mode
def redrawAll(canvas, data):
    if data.mode == "launch":
        launchRedrawAll(canvas,data)
    elif (data.mode == "precut"):
        precutRedrawAll(canvas, data)
    elif (data.mode == "cut"):
        cutRedrawAll(canvas, data)
        canvas.create_text(data.width / 2, data.height - 75, font="Arial "
                                                                   "30 bold",
                           text=
                           data.progressText[1])

    elif (data.mode == "stitch"):
        stitchRedrawAll(canvas, data)
        canvas.create_text(data.width / 2, data.height - 75, font="Arial "
                                                                   "30 bold",
                           text=
                           data.progressText[3])

    elif (data.mode == "extract"):
        extractionRedrawAll(canvas, data)
        canvas.create_text(data.width / 2, data.height - 75, font = "Arial "
                                                                     "30 bold",
                                                                     text=
        data.progressText[2])

    elif (data.mode == "anesthesia"):
        anesthesiaRedrawAll(canvas, data)
        canvas.create_text(data.width / 2, data.height - 75, font="Arial "
                                                                   "30 bold",
                           text=
                           data.progressText[0])
    elif (data.mode == "end"):
        endRedrawAll(canvas,data)

    if data.displayFact == False and len(data.medFacts) > 0:
        print(data.seenFact)
        if data.seenFact %20 == 0:
            canvas.create_rectangle(data.width/7.5 - 100, data.height -50 - 50,
                                    data.width/7.5 + 100, data.height- 50 + 50,
                                    fill = 'gold', outline = '')
            canvas.create_text(data.width/7.5, data.height - 50, font = "Arial 10 "
                                                                       ,
                               fill = 'Black', text =str(data.medFacts.pop(0)))



###############################################################################
                           # LAUNCH SCREEN MODE
###############################################################################

def launchMousePressed(event, data):
    #If select Surgery mode
    if event.x >= data.width/2 + 50 and event.x < data.width/2 + 175 and \
            event.y < data.height/2 + 100 and event.y >= data.height/2 + 50:
        data.currImage = 'images/office.jpg'
        data.mode = "anesthesia"
    #If select Dental mode
    elif event.x >= data.width/2 - 175 and event.x < data.width/2 - 50 and \
            event.y >= data.height / 2 + 50 and event.y < data.height/2 + 100:
        print("dental")
        os.system('python Dental.py')



def launchKeyPressed(event, data):
    pass

#Every time timer fired is called, update Leapmotion data
def launchTimerFired(data):
    launchUpdateLeapMotionData(data)
    launchPrintLeapMotionData(data)

def launchUpdateLeapMotionData(data):
    pass


def launchPrintLeapMotionData(data):
    pass

#CITATION: Creating Rounded rectangles. From StackOverflow,
# https://stackoverflow.com/questions/44099594/how-to
# -make-a-tkinter-canvas-rectangle-with-rounded-corners?rq=1

#Create buttons for Dental/Surgery mode
def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):
    points = (
        x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2,
        y1 + r, x2, y2 - r, x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r,
        y2,
        x1 + r, y2, x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1,
        y1)
    return canvas.create_polygon(points, smooth=True, **kwargs)



def launchRedrawAll(canvas,data):
    #draw Launch screen background
    #CITATION: Creation of image in Tkinter using Python 2.7
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

    boundingBox = canvas.bbox(text)
    rect= canvas.create_rectangle(boundingBox, outline="black",
                                        fill="navy")
    canvas.tag_raise(text, rect)

    #Draw dental and surgery buttons
    drawDentalButton(canvas,data)
    drawSurgeryButton(canvas,data)

#Draw Dental button
def drawDentalButton(canvas,data):
    round_rectangle(canvas, data.width / 2 - 175, data.height / 2 + 50,
                   data.width / 2 - 50,
                   data.height / 2 + 100,
                   fill=
                   "white")
    canvas.create_text(data.width/2 - 110, data.height/2 + 75,font =
    "Arial 20 bold", fill =
    'black', text = "DENTIST")

#Draw Surgery  button
def drawSurgeryButton(canvas,data):
    round_rectangle(canvas, data.width / 2 + 50, data.height / 2 + 50,
                    data.width / 2 + 175,
                    data.height / 2 + 100,
                    fill=
                    "black")
    canvas.create_text(data.width / 2 + 110, data.height / 2 + 75, font =
    "Arial 20  bold", fill=
    'white', text="SURGEON")


###############################################################################
                                #PRECUT MODE
###############################################################################
# mousePressed not used
def precutMousePressed(event, data):
    pass


#keyPressed not used
def precutKeyPressed(event, data):
    pass


def precutTimerFired(data):
    precutUpdateLeapMotionData(data)
    precutPrintLeapMotionData(data)


#Leapmotion to detect if user is using thumb and index to "pinch zoom"
def checkPinchZoom(data, thumb, index):
    tipThumb = thumb.direction
    tipIndex = index.direction
    indexSpeed = index.tip_velocity
    thumbSpeed = thumb.tip_velocity
    print(math.sqrt((indexSpeed[2]) ** 2))
    print(math.sqrt((thumbSpeed[2]) ** 2))
    print('deg', math.degrees(tipThumb.angle_to(tipIndex)))

    #Magnitude of index, thumb velocity must be large enough
    #Angle between index and thumb must be large enough
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
                        # switch to next mode: incision step of surgery
                        data.mode = "cut"




def precutPrintLeapMotionData(data):
    pass


# Draw out initial view of patient
def precutRedrawAll(canvas, data):
    # CITATION: Creation of image in Tkinter using Python 2.7
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




################################################################################
                            # EXTRACTION MODE
################################################################################
# mousePressed not used
def extractionMousePressed(event, data):
    pass

# keyPressed not used
def extractionKeyPressed(event, data):
    pass

#Every time timerFired called, update data
def extractionTimerFired(data):
    extractionUpdateLeapMotionData(data)
    extractionPrintLeapMotionData(data)
    doExtract(data)


# From the precut screen, user can begin surgical procedure by zooming in on
# the patient's wounds through a "pinch" effect detected by leap motion
def extractionUpdateLeapMotionData(data):
    frame = data.controller.frame()
    rightHand = frame.hands.rightmost
    leftHand = frame.hands.leftmost

    left_pointable = leftHand.pointables.frontmost #detected left finger
    right_pointable = rightHand.pointables.frontmost #detected right finger

    app_width = 700
    app_height = 600
    #CITATION: Create 2D interaction box from leapMotion library
    if right_pointable.is_valid or left_pointable.is_valid:
        iBox = frame.interaction_box  # create 2D interaction box with
        leapPointR = right_pointable.stabilized_tip_position
        leapPointL = left_pointable.stabilized_tip_position
        normalizedPointR = iBox.normalize_point(leapPointR, True)
        normalizedPointL = iBox.normalize_point(leapPointL, True)

        app_xL = normalizedPointL.x * app_width #x coord of LH finger
        app_yL = (1 - normalizedPointL.y) * app_height #y coord of LH finger
        app_xR = normalizedPointR.x * app_width #x coord of RH finger
        app_yR = (1 - normalizedPointR.y) * app_height #y coord of RH finger

        #Make right hand image, left hand image follow user's hands
        data.surgRH[0],data.surgRH[1]  = app_xR,app_yR
        data.app_xR, data.app_yR = app_xR, app_yR
        data.surgLH[0],data.surgLH[1] = app_xL,app_yL


#Simulate extraction of foreign objects from patient's wound through hand
# motion
def doExtract(data):
    c = data.controller
    frameCurr = c.frame(0)

    for hand in frameCurr.hands:
        #Check hand validity in current frame
        if hand.is_valid:
            #In order to prepare for extraction, the user must simulate
            # opening up the wound by rotating their hands outwards.
            roll = math.degrees(hand.palm_normal.roll)
            #For right hand, rotate hand outwards to right
            if hand.is_right:
                if roll < - 90 and data.surg[2] < data.width/2 +50:
                    data.surgInstruction = "Keep going!"
                    # print('rollRight')
                    data.surg[2]+=10
            # For left hand, rotate hand outwards to left
            elif hand.is_left:
                if roll > 90 and data.surg[0] > data.width/2  -50:
                    data.surgInstruction = "Keep going!"
                    # print('rollLeft')
                    data.surg[0] -=10



            #Simulate a 3D viewing plane of the wound through hands' motion. By
            # detecting the pitch of the hands (counterclockwise rotation about
            #  the y-axis), the viewing plane will change its orientation.
            pitch= math.degrees(hand.direction.pitch)
            print('pitch deg:', pitch)
            if abs(pitch) > 50:
                if pitch<0: #forwards, top of square's width increases
                  #Tweak polygon (viewing plane) dimensions accordingly for each
                  # degree change in pitch
                  for i in range(int(abs(pitch))):
                    #Keep polygon in bounds
                    if data.surgSquarePoints[0][0] < data.width/2 - 100 and \
                            data.surgSquarePoints[3][0] > data.width/2 + 100:
                        data.surgSquarePoints[0][0] +=0.01
                        data.surgSquarePoints[3][0] -=0.01
                        data.surgSquarePoints[1][0] -= 0.01
                        data.surgSquarePoints[2][0] += 0.01

                        data.surg[1] += 0.005
                else: #backwards, top of square's width decreases
                  # Tweak polygon (viewing plane) dimensions accordingly for
                  # each degree change in pitch
                  for i in range(int(abs(pitch))):
                      # Keep polygon in bounds
                      if data.surgSquarePoints[1][0] < data.width/2 - 100 and \
                              data.surgSquarePoints[2][0] > data.width/2 + 100:
                        (data.surgSquarePoints[1])[0] +=0.01
                        (data.surgSquarePoints[2])[0] -=0.01
                        data.surgSquarePoints[0][0] -= 0.01
                        data.surgSquarePoints[3][0] += 0.01
                        data.surg[1] -= 0.005

    #data.seen ensures that throughout the game, the foreign objects are only
    #  placed once inside the wound.
    if data.seen == 0:
        if data.surg[2] >= data.width/2 + 30 and data.surg[0] <= data.width/2\
                - 30:
            data.surgInstruction = "Wound opened!"
            data.objectBool = True
            #radius of each object is random integer from 15 to 30
            data.size = random.randint(15,30)
            #places foreign objects inside the wound for the user to extract
            placeObject(data)
            data.objectPlaced = True
            #increment data.seen by 1, so although timerFired will be called
            # again, the objects are not placed a second time.
            data.seen+=1
    #After foreign objects placed, user must simulate forceps with their
    # index and thumb finger to extract them.
    if data.objectPlaced == True:
        data.surgInstruction = "Use your index and thumb finger as forceps to remove object."
        data.surgRH[0], data.surgRH[1] = data.width,data.height
        data.surgLH[0], data.surgLH[1] = data.width,data.height
        #Forceps moves with user's right hand
        data.forcepsX = data.app_xR
        data.forcepsY = data.app_yR
        moveForceps(data)
        #Check if forceps are grabbing each object. If yes, the objects are
        # extracted
        for i in data.object:
            if checkCollisionForceps(data, i) == True:
                print("COLLISION")
                if len(data.object) > 0 and i in data.object:
                    data.object.remove(i)
            else:
                pass
    #If all objects extracted, the user has completed the mode successfully.
    if len(data.object) == 0:
        data.surgInstruction = "Great job!"
        data.mode = 'stitch'

#User must manipulate angle between thumb/index to close the forceps around
# the object.
def checkCollisionForceps(data, i ):
        return i[0] - data.size < data.forcepsX and i[0] + \
               data.size\
               > data.forcepsX \
               - 150 and i[1] + data.size <= data.forcepsY and \
               i[1] - data.size >= (
            data.forcepsY + data.fY2)/2


#Change forceps orientation/angle by opening/closing distance between thumb
# and index
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
            #If both thumb/index valid and in frame, forceps can be created
            if thumb in frame.fingers.extended() and index in frame.fingers.extended():
                print("forceps!")
                #Check angle between thumb and index
                data.degrees = math.degrees(dirThumb.angle_to(dirIndex))
                print('degrees', data.degrees)
            #If angle too small to be detected by leapMotion, set it to 0
            if dirThumb.distance_to(dirIndex) < 0.2:
                data.degrees = 0



#For each index in list of objects, set its x and y coordinates to random
# coordinate within wound's boundaries.
def placeObject(data):
    for i in range(len(data.object)):
        data.object[i][1] = random.randint(int(data.surg[1] + 25),
                                         int(data.surg[3]
                                    -25))
        data.object[i][0] = random.randint(int(data.surg[0] + 25),
                                           int(data.surg[2]
                                    - 25))


def extractionPrintLeapMotionData(data):
    pass


#Draw right/left hands
def drawHands(canvas, data):
    #Citation: standard way in python 2.7 to create and resize image
    lh = Image.open('images/surgLH.gif')
    lh0 = lh.resize((200, 350), Image.ANTIALIAS)
    lh1 = ImageTk.PhotoImage(lh0)

    canvas.create_image(data.surgLH[0], data.surgLH[1], image=lh1)
    label = Label(image=lh1)
    label.image = lh1  # keep a reference!

    rh = Image.open('images/surgRH.gif')
    rh0 = rh.resize((200, 350), Image.ANTIALIAS)
    rh1 = ImageTk.PhotoImage(rh0)
    canvas.create_image(data.surgRH[0], data.surgRH[1], image=rh1)
    label = Label(image=rh1)
    label.image = rh1

# Draw out initial view of patient's wound
def extractionRedrawAll(canvas, data):
    canvas.create_rectangle(data.width/2- 350, data.height/2 - 300,
                            data.width/2 + 350, data.height/2+300, fill =
                            'medium sea green')

    canvas.create_polygon(data.surgSquarePoints, fill =
                            'khaki')

    canvas.create_oval(data.surg[0], data.surg[1], data.surg[2], data.surg[3],
        fill = \
        'firebrick',
                           outline = '')

    canvas.create_text(data.width/2, 50, font = "Arial 15 bold", text = \
        data.surgInstruction)

    #If objects have been placed, draw each object in list of objects to be
    # extracted
    for j in range(len(data.object)):
        if data.object[j][0] != None and data.object[j][1] != None and \
            data.objectBool == True:

                canvas.create_oval(data.object[j][0]  - data.size, data.object[j][1] -
                                   data.size,
                                   data.object[j][0] + data.size,data.object[j][1]  +
                                   data.size,
                                   fill = 'gray')


    drawHands(canvas, data)
    #if objects have been Placed, draw forceps
    if data.objectPlaced == True:
        drawForceps(canvas,data)

#Draw a permanently-horizontal line, then a rotatable line that depends on
# the angle between the user's thumb and index fingers to create a pair of
# moveable forceps.
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


############################################################################
                            #ANESTHESIA MODE
############################################################################
# mousePressed not used
def anesthesiaMousePressed(event, data):
    pass

# keyPressed not used
def anesthesiaKeyPressed(event, data):
    pass


# Each time timerFired is called, update data
def anesthesiaTimerFired(data):
    anesthesiaUpdateLeapMotionData(data)
    anesthesiaPrintLeapMotionData(data)
    checkCollisionSyringeBottle(data)


# User must take a syringe and simulate filling up a syringe by following a
# specific thumb press hand orientation.
def anesthesiaUpdateLeapMotionData(data):

    frame = data.controller.frame()  # controller is a Leap.Controller object
    hands = frame.hands
    right = hands.rightmost
    rightFingers = right.fingers
    thumb = rightFingers.finger_type(0)[0]

    rightPosition = right.palm_position
    app_width = 700
    app_height = 600
    # CITATION: create 2D interaction box with
    # dimensions data.width, data.height
    # normalize leap Motion coordinates, map out to Canvas coordinates
    #  app_x and app_y
    iBox = frame.interaction_box
    normalizedPoint = iBox.normalize_point(rightPosition, True)
    app_x = normalizedPoint.x * app_width
    app_y = (1 - normalizedPoint.y) * app_height

    #set hand image's x,y coords to user's hand position as detected by Leap
    data.hand[0] = app_x
    data.hand[1] = app_y
    #User must have thumb up, and press down in order to fill up syringe
    if handCollideSyringe(data) == True:
        print('touched syringe')
        if len(rightFingers.extended()) == 1 and thumb in rightFingers.extended():
            print('correct hand position')
            data.thumb = True
    if data.thumb == True:
            data.hand[2] = 'images/gloverighthold.gif'
            data.syringe[0]  = app_x- 125
            data.syringe[1] = app_y + 50
            data.thumbPressReminder = True
            #Syringe tip must be touching bottle to obtain liquid
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


#Check if hand touching syringe
def handCollideSyringe(data):
    return data.hand[0] >   data.syringe[0] + 25 and data.hand[0] < \
           data.syringe[
               0] + 100 and data.hand[1] > data.syringe[1] - 100 and data.hand[1] < \
                                                 data.syringe[1] - 25

#Check if syringe in contact with anesthesia bottle
def checkCollisionSyringeBottle(data):
    if data.syringe[0] - 70 > data.width / 4 - 20 and data.syringe[0] - 70 < \
            data.width / 4 + 20 and data.syringe[1] + 75 > data.height / 2 + 30 \
            and data.syringe[1] + 75 < data.height / 2 + 90:
        return True
    else:
        return False

#This function detects if user is pressing down their thumb in order to
# simulate using a syringe. The thumb's distal (nearest to tip) and
# intermediate(2nd joint) bones are analyzed, specifically their direction.
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
        #If there is a noticeable angle between thumb's intermediate and
        # distal bone, then the thumb is bent at a certain angle.
        angleInterDistal = dirInterBone.angle_to(dirDistalBone)
        print('angle inter distal:', math.degrees(angleInterDistal))
        if math.degrees(angleInterDistal) > 45:
            return True
        else:
            return False

def anesthesiaPrintLeapMotionData(data):
    pass

#Draw anesthesia mode
def drawBackgroundAnesthesia(canvas,data):
    #Citation: Standard way in python 2.7 to create and resize image through
    # Tkinter
    bg = Image.open('images/office.jpg')
    # resize to fit canvas
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!


    handIm0 = Image.open(data.anesthesiaImage)
    # resize to fit canvas
    handIm = handIm0.resize((100,80), Image.ANTIALIAS)
    handIm2 = ImageTk.PhotoImage(handIm)
    canvas.create_image(data.width - 180, data.height / 2 + 70, image=handIm2)
    label = Label(image=handIm2)
    label.image = handIm2  # keep a reference!

    canvas.create_text(50, 50, font="Arial 15 bold", fill='black', text=
    'Fill up the syringe with anesthetic gel in the bottle!', anchor='w')


#Draw anesthetic bottle
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

#Draw hand image
def drawHand(canvas,data):
    #Citation: standard way in python 2.7 to create/resize image through TKinter
    hand = Image.open(data.hand[2])
    hand1 = hand.resize((200, 150), Image.ANTIALIAS)
    hand2 = ImageTk.PhotoImage(hand1)
    canvas.create_image(data.hand[0], data.hand[1], image=hand2)
    label = Label(image=hand2)
    label.image = hand2  # keep a reference!

#Draw syringe
def drawSyringe(canvas,data):
    # Citation: standard way in python 2.7 to create/resize image through TKinter
    syr = Image.open(data.syringe[2])
    syr2 = syr.resize((200, 200), Image.ANTIALIAS)
    syr3 = ImageTk.PhotoImage(syr2)
    canvas.create_image(data.syringe[0], data.syringe[1], image=syr3)
    label = Label(image=syr3)
    label.image = syr3  # keep a reference!


##############################################################################
                            #INCISION MODE
##############################################################################

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
            #User also fails if they didn't make any incision in the 10 given
            #  seconds
            if data.cut == False:
                data.preCutText = "Try Again!"
                reinitIncisionMode(data)
            elif data.hasFailed == False:
                data.mode = "extract"  # If not failed, advance to next
                # level
            else:
                data.preCutText = "Try Again!"
                reinitIncisionMode(data)

#Reset variables to restart incision mode
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

    # CITATION: Map out leapMotion coordinates to 2D coordinates corresponding
    #  to Canvas dimensions
    if pointable.is_valid:
        iBox = frame.interaction_box
        leapPoint = pointable.stabilized_tip_position

        normalizedPoint = iBox.normalize_point(leapPoint, True)
        app_x = normalizedPoint.x * app_width
        app_y = (1 - normalizedPoint.y) * app_height



        #Hand's grab strength approaches 1 if user makes a clenched fist,
        # and 0 if open hand.
        hand = frame.hands.rightmost
        strength = hand.grab_strength
        # Only able to pick up tool if hand in grasp position
        if strength >0.9:
            data.isGrabbing = True
            print("grabbing")
        else:
            data.isGrabbing = False
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

#Once the scissors touches the dotted line, user can start cutting.
def checkFirstCut(data):
    if data.scissors[2] >= data.dottedLine[0] and data.scissors[2] <= \
            data.dottedLine[2] and data.scissors[3] \
            >= data.dottedLine[1] and data.scissors[3] < \
            data.dottedLine[3]:
        data.cut = True



def cutPrintLeapMotionData(data):
    pass

def drawBackground(canvas,data):
    #Citation: standard way to create/resize images in Python 2.7 through
    # TKinter
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
    #Citation: standard way to create image in Python 2.7 through TKinter
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

    right_pointable = rightHand.pointables.frontmost

    #CITATION: Enable gesture method from leap motion library
    data.controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
    data.controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

    app_width = 700
    app_height = 600
    pointable = right_pointable # finger in most "forward"
    # position
    if data.nextStep != True:
        if pointable.is_valid:
            iBox = frame.interaction_box
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


    #If suture needle tip touches one of the suture points, user is ready to
    # complete suture by piercing the point and tying knot with the wire.
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
                #User rotates left hand in a circular motion to knot wire
                if detectRotate(data) == True:
                    print("CIRCLE DETECTED")
                    data.sutureLines.append([(data.suturePoints[i])[0] - 50,
                                             (data.suturePoints[i])[1],
                                             (data.suturePoints[i])[0],
                                             (data.suturePoints[i])[1]])
                    print('suturelines', len(data.sutureLines))
                    #Moves on to next suture point, if there are any left
                    data.nextStep = False
                    data.sutureInstruction = "Aim suture needle tip to green " \
                                             "dot"
        #If all five stitches completed, user has completed suturing
        if len(data.sutureLines) >= 5:
            data.finishedSuturing = True
            data.sutureInstruction = "WAY TO GO!"
            data.suturingBackground = 'images/finishedSuturing.gif'
            data.nextStep = False
        if data.finishedSuturing == True:
            data.mode = 'end'



#Detect if user rotates their hand in order to simulate tying knot
def detectRotate(data):
    frame = data.controller.frame()
    leftHand = frame.hands.leftmost
    rightHand = frame.hands.rightmost
    for gesture in frame.gestures():
        if gesture.type is Leap.Gesture.TYPE_CIRCLE:
            #Tying knot only done by left hand
            if rightHand not in gesture.hands:
                return True


def stitchPrintLeapMotionData(data):
    pass


def stitchRedrawAll(canvas, data):
    #Citation: standard way to create/resize images in python 2.7 through
    # Tkinter
    bg = Image.open(data.suturingBackground)
    bgIm = bg.resize((700, 600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    canvas.create_text(data.width/2, 50, font = "Arial 25 bold", text =
                                                data.sutureInstruction)

    #Track and output current suturing progress
    if len(data.sutureLines) <5:
        canvas.create_text(data.width / 2, 100, font="Arial 15 bold", text=
        str(5-len(data.sutureLines)) + " left to go!")


    drawSutureNeedle(canvas,data)
    drawSuturePoints(canvas,data)

    #Draw completed suture knots
    for j in range(len(data.sutureLines)):
        [x0,y0,x1,y1] = data.sutureLines[j]
        canvas.create_line(x0,y0,x1,y1, fill = 'mediumpurple1', width = 4)

    drawSutureHands(canvas,data)


def drawSutureHands(canvas,data):
    #Citation:  standard way to create/resize images in python 2.7 through
    # Tkinter
    # LEFTHAND
    rightHand = Image.open('images/sutureHand.gif')
    rightHand1 = rightHand.resize((700, 600), Image.ANTIALIAS)
    rightHand2 = ImageTk.PhotoImage(rightHand1)
    canvas.create_image(data.sutureRightHand[0], data.sutureRightHand[1],
                        image=rightHand2)
    label = Label(image=rightHand2)
    label.image = rightHand2  # keep a reference!

    # LEFTHAND
    leftHand = Image.open('images/leftHand.gif')
    leftHand1 = leftHand.resize((520, 420), Image.ANTIALIAS)
    leftHand2 = ImageTk.PhotoImage(leftHand1)
    canvas.create_image(data.sutureLeftHand[0], data.sutureLeftHand[1],
                        image=leftHand2)
    label = Label(image=leftHand2)
    label.image = leftHand2  # keep a reference!




def drawSutureNeedle(canvas,data):
    # Citation:  standard way to create/resize images in python 2.7 through
    # Tkinter
    needle = Image.open('images/sutureNeedle.gif')
    needle1 = needle.resize((100,220), Image.ANTIALIAS)
    needle2 = ImageTk.PhotoImage(needle1)
    canvas.create_image(data.needle[0], data.needle[1],
                        image=needle2)
    label = Label(image=needle2)
    label.image = needle2


#Draw suture points that needle needs to pierce
def drawSuturePoints(canvas,data):
    print(len(data.suturePoints))
    for i in range(len(data.suturePoints)):
        canvas.create_oval((data.suturePoints[i])[0] - 3,
                           (data.suturePoints[i])[1] -
                           3, (data.suturePoints[0])[0] +3,
                           (data.suturePoints[i])[1] + 3, fill = 'yellow green')


###############################################################################
                           # END SCREEN MODE
###############################################################################

def endMousePressed(event, data):
    pass


def endKeyPressed(event, data):
    if event.keysym == 'p':
        init(data)


def endTimerFired(data):
    endUpdateLeapMotionData(data)


def endUpdateLeapMotionData(data):
    pass
def endRedrawAll(canvas,data):
    end = Image.open('images/doctorlicense.jpg')
    end1 = end.resize((700, 600), Image.ANTIALIAS)
    end2 = ImageTk.PhotoImage(end1)
    canvas.create_image(data.width / 2, data.height / 2, image=end2)
    label = Label(image=end2)
    label.image = end2  # keep a reference!

    canvas.create_text(data.width/2, data.height-100, font =
    "Arial 25 bold", text = "CONGRATULATIONS! Press p to play again")


################################################################################
# use the run function as-is, from 112 Tkinter outline
################################################################################
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
