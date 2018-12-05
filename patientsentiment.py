
import sys

sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")

from Leap.Other import Leap

from Tkinter import *

from PIL import Image, ImageTk


####################################
# customize these functions
####################################

def init(data):
    data.miracle = False
    data.success = False
    data.overHeat = False
    data.countIdle, data.countPersist = 0,0
    data.hand_identifier = None
    data.instructionText = "Maintain the patient's heart rate and temperature!"
    data.failed = False
    data.saved = False
    data.timer = 0
    data.heartRate = 20
    data.temp = 98
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.hand = [data.width/2, data.height-50]
    data.eyeCoord = 10
    data.skinColor = ["floral white", "AntiqueWhite1","bisque2","NavajoWhite2",
                                                                  "PeachPuff2",
    "LightSalmon2",
                      "Salmon2",
                      "IndianRed"]
    data.skinColorIndex = 3
    data.controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)



def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def checkIdle(data):
    previousFrame = data.controller.frame(1)
    if data.hand_identifier != None:
        previousHand = previousFrame.hand(data.hand_identifier)
        prevSpeed = previousHand.palm_velocity
        if abs(prevSpeed[1])<50:
            data.countIdle+=1
            if data.countIdle >= 200:
                overHeatedMode(data)
                data.countIdle = 0

def checkPersist(data):
    previousFrame = data.controller.frame(1)
    if data.hand_identifier != None:
        previousHand = previousFrame.hand(data.hand_identifier)
        prevSpeed = previousHand.palm_velocity
        if (abs(prevSpeed[1])) >50:
            data.countPersist+=1
            if data.countPersist >= 100:
                miracleMode(data)
                data.countPersist = 0

def miracleMode(data):
    data.temp = 99
    data.heartRate = 65
    data.miracle = True

def overHeatedMode(data):
    data.temp +=2.5
    data.heartRate = 150
    data.skinColorIndex = 7
    data.eyeCoord = 12
    data.overHeat = True




def checkSaved(data):
    if 60 <= data.heartRate <100 and 97.5<data.temp <99.5:
        data.success = True
        data.instructionText = "You saved the patient!"



def timerFired(data):
    if data.failed == False and data.success == False and data.overHeat == \
            False and data.miracle == False:
        data.timer += 1
        updateLeapMotionData(data)
        printLeapMotionData(data)
        if data.timer%25 == 0:
            if data.heartRate >=5:
                data.heartRate -=5
            elif 0<=data.heartRate <5:
                data.heartRate = 0
                data.failed = True
        if 0<=data.heartRate < 30:
            data.skinColorIndex = 1
            data.eyeCoord = 2
        elif 30<=data.heartRate <60:
            data.skinColorIndex = 2
            data.eyeCoord = 10
            data.eyeCoord = 3
        elif 60 <= data.heartRate < 100:
            data.skinColorIndex = 3
            data.eyeCoord = 10
        checkIdle(data)
        checkSaved(data)
        checkPersist(data)
    if data.failed == True:
        data.instructionText = "You did not save the patient!"
        data.eyeCoord = 1
        data.skinColorIndex = 0
    elif data.overHeat == True:
        data.instructionText = "You neglected your patient too long and he " \
                               "overheated!"
        data.skinColorIndex = 7
        data.eyeCoord = 15
    elif data.miracle == True:
        data.eyeCoord = 10
        data.skinColorIndex = 3
        data.instructionText = "Your patient was magically cured! \n Perhaps it " \
                               "had something to do with your persistence..."
    elif data.success == True:
        data.eyeCoord = 10
        data.skinColorIndex = 3
        data.instructionText = "You saved the patient!"


handVel = []
def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    rightHand = data.frame.hands.rightmost

    right_pointable = rightHand.pointables.frontmost  # detected right finger

    app_width = 700
    app_height = 600
    # CITATION: Create 2D interaction box from leapMotion library
    if right_pointable.is_valid:
        iBox = data.frame.interaction_box
        leapPointR = right_pointable.stabilized_tip_position
        normalizedPointR = iBox.normalize_point(leapPointR, True)

        app_xR = normalizedPointR.x * app_width  # x coord of RH finger
        app_yR = (1 - normalizedPointR.y) * app_height  # y coord of RH finger
        data.hand[0], data.hand[1] = app_xR, app_yR

    if detectPress(data) == True:
        # print('press!!!')
        if data.heartRate > 0:
            data.heartRate += 2




def controlTemp(data):
    pass
def printLeapMotionData(data):
    pass


def detectPress(data):
    frame = data.controller.frame()
    rightHand = data.frame.hands.rightmost
    data.hand_identifier = rightHand.id
    hand_speed = rightHand.palm_velocity
    # print(hand_speed)
    if rightHand.is_valid and len(frame.fingers.extended()) == 1:
        if hand_speed[1] < -100:
            handVel.append(hand_speed[1])
            return True

def returnPoints():
    return handVel


def redrawAll(canvas, data):
    needle = Image.open('images/hosp.jpg')
    needle1 = needle.resize((700,600), Image.ANTIALIAS)
    needle2 = ImageTk.PhotoImage(needle1)
    canvas.create_image(data.width/2,data.height/2,
                        image=needle2)
    label = Label(image=needle2)
    label.image = needle2



    canvas.create_rectangle(data.width-500, 10, data.width-10,300, fill =
    'gray17')

    canvas.create_text(data.width-250, 25,font = "Arial 20 bold", text = \
        "Heart Rate (bpm): " \
                                                          "" + str(
                                                   data.heartRate),
                       fill = 'green')

    canvas.create_text(data.width - 250, 50, font="Arial 20 bold", text= \
        "Temp (F): " \
        "" + str(
           data.temp),
                       fill='blue')
    canvas.create_oval(data.width/2-80,data.height/2-40,
                       data.width/2+120,data.height/2 + 160 ,
                       fill =data.skinColor[data.skinColorIndex])


    canvas.create_oval(data.width/1.75- 5, data.height/2 + 50
                       -data.eyeCoord, data.width/1.75
                       +5, data.height/2+50 +data.eyeCoord, fill = 'black')

    canvas.create_oval(data.width / 2 - 5, data.height / 2 + 50
                       - data.eyeCoord, data.width / 2
                       + 5, data.height / 2 + 50 + data.eyeCoord, fill='black')

    canvas.create_line(data.width/2,data.height/2+100 , data.width/1.75,
                       data.height/2 +100)

    if data.skinColorIndex == 3:
        smile = data.width / 2 + 65, data.width / 2 + 75, data.height / 2 + 35, \
                data.height / 2 + 40
        canvas.create_arc(smile, start=-180, extent=180, fill="salmon")

    if data.overHeat == True:
        canvas.create_oval(data.width/2-10, data.height/2+70,
                           data.width/2
                           +60, data.height/2+120, fill = 'salmon')

    end = Image.open('images/twoHands.gif')
    end1 = end.resize((300,200), Image.ANTIALIAS)
    end2 = ImageTk.PhotoImage(end1)
    canvas.create_image(data.hand[0], data.hand[1],image=end2)
    label = Label(image=end2)
    label.image = end2  # keep a reference!

    canvas.create_text(data.width / 2, data.height - 70, font='Arial 25 '
                                                              'bold', text=str(
        data.instructionText), fill='black')


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
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700,600)

