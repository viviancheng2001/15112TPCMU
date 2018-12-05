###############################################################################

# CITATION: Created using outline of providedStarterFile leapMotionDemo.py
# which includes:
# LeapMotion built-in variables/gesture-detection functions from leap
# motion library
# 112 Tkinter Framework, from the CMU 15-112 course

#Implements functions from leapMotion database to obtain hand data
###############################################################################

# ]import Leap, sys, thread, time
import sys

import random

sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")

from Leap.Other import Leap
from Leap.Other.Leap import SwipeGesture

from Tkinter import *

from PIL import Image, ImageTk


####FingerCounter class############################################

# CITATION: FingerCounter class from LeapMotion library

class FingerCounter(Leap.Listener):
    def on_frame(self, controller):
        f = controller.frame()
        extended = (len(f.fingers.extended()))
        return extended  # returns number of extended fingers detected by Leap


listener = FingerCounter()

try:
    controller = Leap.Controller()
    controller.add_listener(listener)
except KeyboardInterrupt:
    pass
finally:
    controller.remove_listener(listener)

    # *************************************************************************

    # Use swipe detection to change between surgical tools
    #######SWIPING SETUP##############

    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)  # new
    controller.config.set("Gesture.Swipe.MinLength", 100.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 750)
    controller.config.save()




#######SWIPING SETUP##############

def init(data):
    data.teethInstructions = ["Cleaned STAINED teeth with "
                              "toothbrush",  "Don't touch ANY teeth with "
                                             "mirror!",
                              "Remove ROTTEN teeth with drill"]
    data.toolWidth = 175
    data.wrongTool = False
    data.toolHeight = 190
    data.won = False  # if complete task successfully
    data.gameOver = False  # if failed
    data.backgroundColor = 'sky blue'
    data.isGrabbing = False
    data.fingerCounter = FingerCounter()  # new instance FingerCounter
    data.controller = Leap.Controller()  # new instance controller
    data.toolIndex = 0
    data.handGrasp = [data.width / 2, data.height / 2, 'images/handgrasp.gif']
    # creates virtual hand
    data.timerDelay = 100
    data.timer = 0
    data.frame = data.controller.frame()  # new frame
    # list of surgical tools
    data.tools = [['Toothbrush', 'images/brush.gif', data.width - 200,
                   data.height - 175], ['Mirror', 'images/mirror.gif',
                                        data.width - 200,
                                        data.height - 175], ["Drill",
                                                             'images/drill2.gif',
                                                             data.width - 200,
                                                             data.height - 175
                                                             ]]
    data.toolWidth = 175
    data.toolHeight = 190

    data.topTeeth = [[0, 0, 0, 0, 0]] * 5  # list of patient's teeth
    data.margin = data.width / 2 - 100
    for i in range(len(data.topTeeth)):
        x0 = data.margin + (i * 40)
        y0 = data.height / 7
        x1 = data.margin + ((i + 1) * 40)
        y1 = data.height / 7 + 35
        # Random level of cleanliness for each tooth
        (data.topTeeth[i]) = [x0, y0, x1, y1, random.choice(['khaki', 'snow',
                                                             'gray17'])]


def mousePressed(event, data):
    pass


def keyPressed(event, data):
    if event.keysym == "r":
        init(data)


def timerFired(data):
    updateLeapMotionData(data)
    printLeapMotionData(data)

########Check if grabbing/making a fist, which allows us to pick up and
            # move around surgical tool###########
def isGrasping(data):

    frame = data.controller.frame()
    hand = frame.hands.rightmost
    strength = hand.grab_strength
    if strength > 0.8:
        data.isGrabbing = True
        print('grabbing')
    elif strength < 0.2:
        data.isGrabbing = False
        print('not grabbing')
    return data.isGrabbing

########### CHECK DENTAL TOOL COLLISION WITH TOOTH  #############
def checkToolCollisionWithTooth(data, tooth):
    if (data.tools[data.toolIndex])[2] + data.toolWidth / 2 - \
            10 > tooth[
        0] and (
            data.tools[data.toolIndex])[2] + data.toolWidth / 2 \
            - 10 < tooth[2] and \
            (data.tools[
                data.toolIndex])[3] - data.toolHeight / 2 + 10 > \
            tooth[1] \
            and (data.tools[data.toolIndex])[3] - \
            data.toolHeight / 2 + 10 \
            < tooth[3]:
        print('collision!')
        return True
    else:
        return False

########### CHECK IF USING CORRECT TOOL FOR CORRECT TEETH#############
def useCorrectTool(data,tooth):
    if tooth[4] == 'gray17':
        return (data.tools[data.toolIndex])[0] == 'Drill'
    elif tooth[4] == 'khaki':
        return (data.tools[data.toolIndex])[0] == "Toothbrush"
    elif tooth[4] == 'white smoke':
        return True
    else:
        return False


########### REMOVE / CLEAN TEETH #############
def doProcedure(data, tooth):
    if tooth[4] == 'gray17':
        print('removing rotten tooth')
        data.topTeeth.remove(tooth)
    elif tooth[4] == 'khaki':
        print("cleaning stained tooth")
        tooth[4] = 'white smoke'
    elif tooth[4] == 'white smoke':
        pass
    else:
        data.gameOver = True
###########  DETECTS SWIPE TO CHANGE TOOL  #############
def detectSwipe(data):
    frame = data.controller.frame()
    for gesture in frame.gestures():
        if gesture.type == Leap.Gesture.TYPE_SWIPE:
            swipe = SwipeGesture(gesture)
            # "Wraparound" tools once reach end of tools list
            if data.toolIndex == len(data.tools) - 1:
                data.toolIndex = 0
            else:
                data.toolIndex += 1
            print(data.tools[data.toolIndex])
            print "SWIPING: Swipe id: %d, state: %s, position: %s, " \
                  "direction: " \
                  "%s, speed: %f" % (
                      gesture.id, (gesture.state),
                      swipe.position, swipe.direction, swipe.speed)

########### CHECK IF USER HAS SUCCESSFULLY COMPLETED TASK #############

def checkGameOver(data):
    countTeeth = 0
    for t in data.topTeeth:
        if t[4] != 'snow' and t[4] != 'white smoke':
            countTeeth += 1
    # If no dirty teeth remaining, user has completed the surgery successfully
    if countTeeth == 0:
        data.won = True
    return data.won


# Maps out hand location detected by LeapMotion to 2D coordinates on Canvas
def updateLeapMotionData(data):
    if data.gameOver == False and data.won == False:  # if task not ended yet
        data.timer += 1
        frame = data.controller.frame()
        app_width = 700
        app_height = 600
        pointable = frame.pointables.frontmost  # finger in most "forward"
        # position

        if pointable.is_valid:
            iBox = frame.interaction_box  # create 2D interaction box with
            # dimensions data.widthxdata.height
            # normalize leap Motion coordinates, map out to Canvas coordinates
            #  app_x and app_y
            leapPoint = pointable.stabilized_tip_position
            normalizedPoint = iBox.normalize_point(leapPoint, True)
            app_x = normalizedPoint.x * app_width
            app_y = (1 - normalizedPoint.y) * app_height
            print ("X: " + str(app_x) + " Y: " + str(app_y))

            data.handGrasp[0] = app_x
            data.handGrasp[1] = app_y

            if isGrasping(data) == True:

            # if user making grasp motion, make virtual tool follow his/her
            # hand around
                (data.tools[data.toolIndex])[2] = app_x
                (data.tools[data.toolIndex])[3] = app_y
                for tooth in data.topTeeth:
                    if checkToolCollisionWithTooth(data,tooth) == True:
                        if useCorrectTool(data, tooth) == True:
                            doProcedure(data,tooth)
                        else: #if use wrong tool
                            if tooth[4] != 'snow':
                                data.wrongTool = True
                            else: #cannot touch white teeth
                                data.gameOver = True
            else:
                #If hand not in grasp position, cannot pick up tool
                (data.tools[data.toolIndex])[2]= data.width-200
                (data.tools[data.toolIndex])[3] =  data.height-175

        detectSwipe(data)


def printLeapMotionData(data):
    pass


def drawTeeth(canvas,data):
    for i in range(len((data.topTeeth))):
        x0 = (data.topTeeth[i])[0]
        y0 = (data.topTeeth[i])[1]
        x1 = (data.topTeeth[i])[2]
        y1 = (data.topTeeth[i])[3]
        canvas.create_rectangle(x0, y0, x1, y1, fill=data.topTeeth[i][4])

    # Draw one tool at a time based on current toolIndex
    t = Image.open((data.tools[data.toolIndex])[1])
    t2 = t.resize((175, 190), Image.ANTIALIAS)
    toolImg = ImageTk.PhotoImage(t2)
    canvas.create_image(((data.tools[data.toolIndex])[2]),
                        (data.tools[data.toolIndex])[3],
                        image=
                        toolImg)
    label = Label(image=toolImg)
    label.image = toolImg  # keep a reference!

def drawHand(canvas,data):
    handGrasp = Image.open(data.handGrasp[2])
    handGrasp2 = handGrasp.resize((250,250), Image.ANTIALIAS)
    handGrasp3 = ImageTk.PhotoImage(handGrasp2)
    canvas.create_image(data.handGrasp[0], data.handGrasp[1], image=handGrasp3)
    label = Label(image=handGrasp3)
    label.image = handGrasp3



def drawBackground(canvas,data):
    bg = Image.open('images/dent1.jpg')
    # resize to fit canvas
    bgIm = bg.resize((700, 650), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width / 2, data.height / 2, image=bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    # Background image: default image of a patient's open mouth
    mouth = Image.open('images/openmouth.gif')
    # resize to fit canvas
    mouth2 =mouth.resize((650, 650), Image.ANTIALIAS)
    mouth3 = ImageTk.PhotoImage(mouth2)
    canvas.create_image(data.width / 2, data.height / 2, image=mouth3)
    label = Label(image=mouth3)
    label.image = mouth3 # keep a reference!
def drawInstructions(canvas,data):
    canvas.create_text(data.width / 2, 40, font="Arial 50 bold", text=
    "Dental Mode", fill = 'RoyalBlue1')
    canvas.create_text(data.width - 200, data.height - 75, font="Arial 20 bold",
                       text='Swipe to change tool')
    canvas.create_text(data.width - 200, data.height - 50, font="Arial 15 "
                                                                "bold", text=
                       "You are using the %s" % data.tools[data.toolIndex][0])

    # Instructions for user

    canvas.create_text(30, data.height - 75, font = "Arial 18 bold",
                       text=' ' \
                                                                    'NAVIGATE HAND TO GRASP TOOL.', anchor ='w')
    canvas.create_text(30, data.height - 50, font="Arial 18 bold",
                           text= data.teethInstructions[data.toolIndex],
                       fill = 'Red', anchor = 'w')


def redrawAll(canvas, data):

    drawBackground(canvas,data)
    drawInstructions(canvas,data)
    # Draw top teeth based on stored x/y coordinates in list and color
    drawTeeth(canvas,data)
    # Draw virtual hand
    drawHand(canvas,data)

    ############Checking Game Over####################
    if checkGameOver(data) == True:
    # Draw winning graphics
        drawWon(canvas,data)
    # Else draw losing graphics
    if data.gameOver == True:
        drawGameOver(canvas,data)

    if data.wrongTool == True:

        canvas.create_text(data.width / 2, data.height / 2 + 100, font="Arial "
                                                                       "60 "
                                                                       "bold",
                           text="WRONG TOOL!",
                           fill='red')
        data.wrongTool = False

def drawWon(canvas,data):
    happyTooth = Image.open('images/happyToothGameOver.gif')
    happyTooth2 = happyTooth.resize((500, 500), Image.ANTIALIAS)
    happyTooth3 = ImageTk.PhotoImage(happyTooth2)
    canvas.create_image(data.width / 2, data.height / 2,
                        image=happyTooth3)
    label = Label(image=happyTooth3)
    label.image = happyTooth3
    canvas.create_text(data.width / 2, data.height / 2 + 100, font="Arial "
                                                                   "60 "
                                                                   "bold",
                       text="NICE JOB!",
                       fill='lime green')

def drawGameOver(canvas,data):
    sadTooth = Image.open('images/sadToothGameOver.gif')
    sadTooth2 = sadTooth.resize((500, 500), Image.ANTIALIAS)
    sadTooth3 = ImageTk.PhotoImage(sadTooth2)
    canvas.create_image(data.width / 2, data.height / 2,
                        image=sadTooth3)
    label = Label(image=sadTooth3)
    label.image = sadTooth3
    canvas.create_text(data.width / 2, data.height / 2 + 100, font="Arial "
                                                                   "60 "
                                                                   "bold",
                       text="GAME OVER",
                       fill='red')
    canvas.create_text(data.width / 2, data.height / 2 + 150, font="Arial "
                                                                   "20 "
                                                                   "bold",
                       text="Press r to restart",
                       fill='red')


####################################
# use the run function as-is
####################################


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
    data.timerDelay = 5  # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    timerFiredWrapper(canvas, data)

    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(700, 600)
