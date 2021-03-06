#]import Leap, sys, thread, time
import sys

import random
sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")

import Leap
from Leap import SwipeGesture

from Tkinter import *

from PIL import Image, ImageTk


####################################
# customize these functions
####################################


class FingerCounter (Leap.Listener):
    def on_frame (self, controller):
        f = controller.frame()
        extended = (len(f.fingers.extended()))
        return extended

listener = FingerCounter()

try:
    controller = Leap.Controller()
    controller.add_listener(listener)
except KeyboardInterrupt:
    pass
finally:
    controller.remove_listener(listener)




# *****************************************************************************************


#######SWIPING SETUP##############

    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE) #new
    controller.config.set("Gesture.Swipe.MinLength", 100.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 750)
    controller.config.save()

#######SWIPING SETUP##############

def init(data):
    data.won = False
    data.gameOver = False
    data.backgroundColor = 'lemon chiffon'
    data.isGrabbing = False
    data.fingerCounter = FingerCounter()
    data.controller = Leap.Controller()
    data.toolIndex = 0
    data.handGrasp = [data.width/2,data.height/2, 'images/handgrasp.gif']



    data.timerDelay = 100
    data.timer = 0
    data.frame = data.controller.frame()
    data.tools = [['Toothbrush','images/brush.gif', data.width-200,
                   data.height-175],['Mirror','images/mirror.gif',
                                     data.width-200,
                                     data.height-175],["Drill",
                                                       'images/drill.gif',
                                                       data.width-200,
                                                       data.height-175
  ]]
    #x-y coord
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']


    data.topTeeth = [[0,0,0,0,0]]*5
    data.margin = data.width/2 - 100
    for i in range(len(data.topTeeth)):
        x0 = data.margin + (i*40)
        y0 = data.height/7
        x1 = data.margin + ((i+1)*40)
        y1 = data.height/7 + 35
        print(x0,y0,x1,y1)
        (data.topTeeth[i])= [x0,y0,x1,y1, random.choice(['khaki','snow',
                                                         'gray17'])]

    print(data.topTeeth)


def mousePressed(event, data):
    pass
        # if event.x > i[0] and event.x< i[2] and event.y>i[1] and event.y <i[3]:
        #     if len(data.topTeeth) >0:
        #         data.topTeeth.remove(i)


def keyPressed(event, data):
    pass

def timerFired(data):
    updateLeapMotionData(data)
    printLeapMotionData(data)



def updateLeapMotionData(data):
    if data.gameOver == False and data.won == False:
        data.timer+=1
        frame = data.controller.frame()
        app_width = 700
        app_height = 600
        pointable = frame.pointables.frontmost

        if pointable.is_valid:
            iBox = frame.interaction_box
            leapPoint = pointable.stabilized_tip_position

            normalizedPoint = iBox.normalize_point(leapPoint,True)
            app_x = normalizedPoint.x * app_width
            app_y = (1-normalizedPoint.y) * app_height


            print ("X: " + str(app_x) + " Y: " + str(app_y))
            hand = frame.hands.rightmost
            strength = hand.grab_strength
            data.handGrasp[0] = app_x
            data.handGrasp[1] = app_y
            if strength > 0.8:
                data.isGrabbing = True
                print('grab')
            elif strength < 0.3:
                data.isGrabbing = False
                print('not grab')

            if data.isGrabbing == True:
                (data.tools[data.toolIndex])[2] = app_x
                (data.tools[data.toolIndex])[3] = app_y
                for tooth in data.topTeeth:
                    if (data.tools[data.toolIndex])[2] > tooth[0]  and (
                            data.tools[data.toolIndex])[2]<tooth[2] and (data.tools[
                        data.toolIndex])[3] > tooth[1]\
                            and (data.tools[data.toolIndex])[3]< tooth[3] :
                        if tooth[4] == 'gray17':
                            print('removing rotten tooth')
                            data.topTeeth.remove(tooth)
                        elif tooth[4] == 'khaki':
                            tooth[4] = 'white smoke'
                        elif tooth[4] == 'white smoke':
                            continue
                        else:
                            data.gameOver = True
            else:
                (data.tools[data.toolIndex])[2]= data.width-200
                (data.tools[data.toolIndex])[3] =  data.height-175








        if data.timer % 10 == 0:
            print(data.fingerCounter.on_frame(data.controller))
            if data.fingerCounter.on_frame(controller) == 2:
                if len(data.topTeeth) > 0:
                    pass



    ######gestures#########
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                if data.toolIndex == len(data.tools) -1:
                    data.toolIndex = 0
                else:
                    data.toolIndex+=1
                print(data.tools[data.toolIndex])
                print "SWIPE BITCH Swipe id: %d, state: %s, position: %s, " \
                      "direction: " \
                      "%s, speed: %f" % (
                    gesture.id, (gesture.state),
                    swipe.position, swipe.direction, swipe.speed)

def printLeapMotionData(data):
    pass


def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill=
    data.backgroundColor)

    bg = Image.open('images/openmouth.gif')
    bgIm = bg.resize((600,600), Image.ANTIALIAS)
    bgIm2 = ImageTk.PhotoImage(bgIm)
    canvas.create_image(data.width/2, data.height/2,image = bgIm2)
    label = Label(image=bgIm2)
    label.image = bgIm2  # keep a reference!

    data.margin = data.width/2 - 150
    r = 150

    # canvas.create_oval(data.width/2 - r, 2*data.height/5- r, data.width/2 + r,
    #                    2*data.height/5+ r, fill = 'pink')
    for i in range(len((data.topTeeth))):
        x0 = (data.topTeeth[i])[0]
        y0 = (data.topTeeth[i])[1]
        x1 = (data.topTeeth[i])[2]
        y1 = (data.topTeeth[i])[3]
        canvas.create_rectangle(x0,y0,x1,y1,fill = data.topTeeth[i][4])
    # canvas.create_image(0,0,data.width/2, data.height/2,image =
    #    photo)

    t = Image.open((data.tools[data.toolIndex])[1])
    t2 = t.resize((175,190), Image.ANTIALIAS)
    toolImg = ImageTk.PhotoImage(t2)
    canvas.create_image(((data.tools[data.toolIndex])[2]),(data.tools[data.toolIndex])[3],
                        image =
    toolImg)
    label = Label(image=toolImg)
    label.image = toolImg # keep a reference!

    handGrasp = Image.open(data.handGrasp[2])
    handGrasp2 = handGrasp.resize((125, 125), Image.ANTIALIAS)
    handGrasp3 = ImageTk.PhotoImage(handGrasp2)
    canvas.create_image(data.handGrasp[0], data.handGrasp[1], image=handGrasp3)
    label = Label(image=handGrasp3)
    label.image = handGrasp3

    # label.pack()
    canvas.create_text(30, data.height - 65, text=' Navigate hand to grasp '
                                                  'tool.\n Remove rotten '
                                                  'teeth, clean stained \n '
                                                  'teeth, and don''t touch '
                                                  'white teeth!', anchor = 'w')

    countTeeth = 0
    for t in data.topTeeth:
        if t[4] !='snow' and t[4] != 'white smoke':
            countTeeth +=1
    if countTeeth == 0:
        data.won = True
    if data.won == True:
        happyTooth = Image.open('images/happyToothGameOver.gif')
        happyTooth2 = happyTooth.resize((500, 500), Image.ANTIALIAS)
        happyTooth3 = ImageTk.PhotoImage(happyTooth2)
        canvas.create_image(data.width / 2, data.height / 2,
                            image=happyTooth3)
        label = Label(image=happyTooth3)
        label.image = happyTooth3
        canvas.create_text(data.width / 2, data.height / 2 +100, font="Arial "
                                                                       "60 "
                                                                       "bold",
                           text="NICE JOB!",
                           fill= 'lime green')
    if data.gameOver == True:
        sadTooth = Image.open('images/sadToothGameOver.gif')
        sadTooth2 = sadTooth.resize((500,500), Image.ANTIALIAS)
        sadTooth3 = ImageTk.PhotoImage(sadTooth2)
        canvas.create_image(data.width/2,data.height/2,
                            image= sadTooth3)
        label = Label(image=sadTooth3)
        label.image = sadTooth3
        canvas.create_text(data.width / 2, data.height / 2 + 100, font="Arial "
                                                                      "60 "
                                                                 "bold",
                           text="BAD DOCTOR",
                           fill='red')







    canvas.create_text(data.width/2, 25, font = "Arial 50 bold", text =
    "Dental Mode")
    canvas.create_text(data.width -200, data.height-75, font="Arial 20 bold",
                       text='Swipe to change tool')
    canvas.create_text(data.width - 200,data.height-50,font = "Arial 15 "
                                                              "bold", text =
    "You are using the %s" % data.tools[data.toolIndex][0])

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

    timerFiredWrapper(canvas,data)


    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700,600)

