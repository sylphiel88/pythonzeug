from threading import Timer,Thread,Event
from tkinter import Tk, Label,PhotoImage,Canvas
from threading import Timer
import random
from PIL import Image, ImageTk

class snake:
    def __init__(self):
        self.len = 6
        self.fields = [[13,12],[14,12],[15,12],[16,12],[17,12],[18,12]]
        self.dir='w'

    def placeSnake(self,mainFields):
        img_b = PhotoImage(file='sn_body.png')
        img_h = PhotoImage(file='sn_head.png')
        img_t = PhotoImage(file='sn_tail.png')
        for i in range(self.len):     
            x = self.fields[i][0]
            y = self.fields[i][1]
            img = img_b
            if i == 0:
                img = img_h
            elif i==self.len-1:
                img = img_t
            mainFields[x][y].configure(image=img)
            mainFields[x][y].image=img
    
    def deleteImages(self, mainFields):
        for i in range(self.len):
            x = self.fields[i][0]
            y = self.fields[i][1]
            mainFields[x][y].configure(image='')
            mainFields[x][y].image=''
    def collisonControll(self, mainField):
        global currFruit, fruitEaten
        c = 0
        for i in range(self.len):
            if self.fields[0]==self.fields[i]:
                c+=1
            if c==2:
                gameOverL = Label()
                gameOverP = PhotoImage(file='sn_go.png')
                gameOverL.configure(image=gameOverP)
                gameOverL.place(x=425,y=200)
                t.cancel()
        if self.fields[0][0] == currFruit.x and self.fields[0][1]==currFruit.y:
            mainFields[currFruit.x][currFruit.y].configure(image='')
            mainFields[currFruit.x][currFruit.y].image=''
            fruitEaten = True
            while [currFruit.x,currFruit.y] in self.fields:
                currFruit=Fruit()
                currFruit.paint(mainFields)
                self.deleteImages(mainFields)
                self.placeSnake(mainFields)
        if self.fields[0][0] == 0 or self.fields[0][0] == 29 or self.fields[0][1] == 0 or self.fields[0][1] == 24:
            imP = PhotoImage(file='sn_go.png')
            imL = Label(image=imP,bg='grey')
            imL.image=imP
            imL.place(x=250,y=250)

class Fruit:
    def __init__(self):
        self.x = random.randint(1,28)
        self.y = random.randint(1,23)
    def paint(self, mainFields):
        img = PhotoImage(file='sn_fruit.png')
        mainFields[self.x][self.y].configure(image=img)
        mainFields[self.x][self.y].image=img


speed = 0.1

root = Tk()
root.title('Snake')
root.config(bg='black')
root.geometry('850x775')

class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")

atleastonemove = False

def timeout():
    global atleastonemove, fruitEaten
    if theSnake.dir=='w':
        theSnake.deleteImages(mainFields)
        if fruitEaten==True:
            fruitEaten=False
            theSnake.len+=1
            print(theSnake.len)
        else:
            theSnake.fields.pop(theSnake.len-1)
        tempx=theSnake.fields[0][0]-1
        tempy=theSnake.fields[0][1]
        theSnake.fields.insert(0,[tempx,tempy])
        theSnake.placeSnake(mainFields)
        atleastonemove = True
        theSnake.collisonControll(mainFields)
    if theSnake.dir=='e':
        theSnake.deleteImages(mainFields)
        if fruitEaten==True:
            fruitEaten=False
            theSnake.len+=1
            print(theSnake.len)
        else:
            theSnake.fields.pop(theSnake.len-1)  
        tempx=theSnake.fields[0][0]+1
        tempy=theSnake.fields[0][1]
        theSnake.fields.insert(0,[tempx,tempy])
        theSnake.placeSnake(mainFields)
        atleastonemove = True
        theSnake.collisonControll(mainFields)
    if theSnake.dir=='n':
        theSnake.deleteImages(mainFields)
        if fruitEaten==True:
            fruitEaten=False
            theSnake.len+=1
            print(theSnake.len)
        else:
            theSnake.fields.pop(theSnake.len-1)
        tempx=theSnake.fields[0][0]
        tempy=theSnake.fields[0][1]-1
        theSnake.fields.insert(0,[tempx,tempy])
        theSnake.placeSnake(mainFields)
        atleastonemove = True
        theSnake.collisonControll(mainFields)
    if theSnake.dir=='s':
        theSnake.deleteImages(mainFields)
        if fruitEaten==True:
            fruitEaten=False
            theSnake.len+=1
            print(theSnake.len)
        else:
            theSnake.fields.pop(theSnake.len-1)
        tempx=theSnake.fields[0][0]
        tempy=theSnake.fields[0][1]+1
        theSnake.fields.insert(0,[tempx,tempy])
        theSnake.placeSnake(mainFields)
        atleastonemove = True
        theSnake.collisonControll(mainFields)
    


t = InfiniteTimer(speed, timeout)
t.start()


def keypressedW(event):
    global atleastonemove
    if (theSnake.dir=='w' or theSnake.dir=='e') and atleastonemove:
        theSnake.dir = 'n'
        atleastonemove = False

def keypressedS(event):
    global atleastonemove
    if (theSnake.dir=='w' or theSnake.dir=='e') and atleastonemove:
        theSnake.dir = 's'
        atleastonemove = False
        theSnake.collisonControll(mainFields)

def keypressedA(event):
    global atleastonemove
    if theSnake.dir=='n' or theSnake.dir=='s':
        theSnake.dir = 'w'
        atleastonemove = False
        theSnake.collisonControll(mainFields)
def keypressedD(event):
    global atleastonemove
    if theSnake.dir=='n' or theSnake.dir=='s':
        theSnake.dir = 'e'
        atleastonemove = False
        theSnake.collisonControll(mainFields)

root.bind('w', keypressedW)
root.bind('s', keypressedS)
root.bind('a', keypressedA)
root.bind('d', keypressedD)

heading = Label(bg="#000000", text='Snake', fg='#FFFFFF')
heading.place(x=0,y=0, width=850,height=50)

mainField = Label(bg='#555555', text='')
mainField.place(x=50, y=50, width=752, height=627)



mainFields = [[]]


for i in range(30):
    tempFields = []
    for j in range(25):
        if i==0 or i==29 or j==0 or j==24:
            tempLabel=Label(mainField, bg='#101010')
            tempLabel.grid(column=i, row=j)
            tempLabel.place(x=25*i,y=25*j,width=23,height=23)
            tempFields.append(tempLabel)
        else:
            tempLabel=Label(mainField, bg='#333333')
            tempLabel.grid(column=i, row=j)
            tempLabel.place(x=25*i,y=25*j,width=23,height=23)
            tempFields.append(tempLabel)
    mainFields.append(tempFields)
mainFields.pop(0)

fruitEaten = False
theSnake = snake()
currFruit=Fruit()

currFruit.paint(mainFields)
theSnake.placeSnake(mainFields)
root.mainloop()