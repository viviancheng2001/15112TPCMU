###############################################################################

# CITATION: Created using outline of provided starterFile leapMotionDemo.py

###############################################################################

import sys

sys.path.insert(0, "/Users/viviancheng/Desktop/LeapSDK/lib/x86")

from Leap.Other import Leap

from Tkinter import *

from PIL import Image, ImageTk


# Counts number of fingers extended
class FingerCounter(Leap.Listener):
    def on_frame(self, controller):
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

    #######SWIPING SETUP##############

    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)  # new
    controller.config.set("Gesture.Swipe.MinLength", 100.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 750)
    controller.config.save()


# Move to next question by swiping, number fingers determines answer
# import mcat dataset?

def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):
    points = (
        x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2,
        y1 + r, x2, y2 - r, x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r,
        y2,
        x1 + r, y2, x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1,
        y1)
    return canvas.create_polygon(points, smooth=True, **kwargs)


def init(data):
    data.progressRect = []
    data.permRect = []
    data.progress = 70
    data.timerDelay = 500
    data.isCorrect = None
    data.timer = 0
    data.questionNumber = 1
    data.fingerCounter = FingerCounter()
    data.controller = Leap.Controller()
    data.questions = ["Experiments using the two mutant strains P and Q \n"
                      "reveal that strain P accumulates citrulline,but strain Q"
                      " does not. \nWhich of the following statements is "
                      "\nmost "
                      "consistent with the data provided?"]
    data.answerChoices = ['1) Strain Q has only one mutation.\n '
                          '2) Strain P has a mutation in argF only. \n'
                          '3) Strain P has a mutation in argG only.\n'
                          '4) Strain P has mutations in argF, argG and argH.']
    data.correctAnswers = [3]


def mousePressed(event, data):
    pass


def keyPressed(event, data):
    pass


def timerFired(data):
    updateLeapMotionData(data)
    printLeapMotionData(data)


def updateLeapMotionData(data):
    data.timer += 1
    if data.progress + 3 <= 178:
        data.progress += 2.5
    if data.progress >= 180:
        data.isCorrect = False
    if data.timer % 10 == 0:
        frame = data.controller.frame()
        if not frame.hands.is_empty:
            hand = frame.hands[0]
            fingers = hand.fingers
            if not fingers.is_empty:
                numFingersExtended = data.fingerCounter.on_frame(
                    data.controller)
                print(numFingersExtended)
                if numFingersExtended == data.correctAnswers[0]:
                    data.isCorrect = True
                    data.resultText = "Correct!"
                    # data.correctAnswers.pop()
                else:
                    data.isCorrect = False
                    data.resultText = "Wrong!"


def printLeapMotionData(data):
    pass


def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill=
    'lavender')

    canvas.create_text(data.width - 180, 35,
                       font="Arial 15 bold",
                       text="Time Remaining:    ", anchor="e")
    canvas.create_text(data.width / 2, data.height / 2 - 200,
                       font="Arial 20 bold",
                       text="Q" + str(data.questionNumber) + ": " +
                            data.questions[0])
    canvas.create_text(data.width / 2, data.height / 2 - 100,
                       font="Arial 15 italic",
                       text="**Hold up number of fingers of correct answer**",
                       fill='gray31')
    round_rectangle(canvas, data.width - 180, 20, data.width - 70, 45, fill=
    "white")
    round_rectangle(canvas, data.width - 180, 20, data.width - data.progress,
                    45,
                    fill=
                    "spring green")
    cit = Image.open('images/citrulline.gif')
    cit1 = cit.resize((300, 100), Image.ANTIALIAS)
    cit2 = ImageTk.PhotoImage(cit1)
    canvas.create_image(data.width / 2, data.height / 2, image=cit2)
    label = Label(image=cit2)
    label.image = cit2
    canvas.create_text(data.width / 2, data.height / 2 + 150, text= \
        data.answerChoices[0], font='Arial 20', fill='gray17')

    if data.isCorrect == True:
        canvas.create_text(data.width / 2, data.height / 2 - 100,
                           font="Arial 30 bold",
                           text="Correct!", fill='dark green')

        canvas.create_text(data.width / 2, data.height / 2 + 150, text= \
            data.answerChoices[0], font='Arial 20', fill='gray17')
    elif data.isCorrect == False:
        canvas.create_text(data.width / 2, data.height / 2 - 100,
                           font="Arial 30 bold",
                           text="Wrong", fill='red')

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
    data.timerDelay = 20  # milliseconds
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
