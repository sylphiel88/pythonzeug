from tkinter import Tk, Frame, Button, Label, Canvas, StringVar, Entry, Checkbutton, IntVar
from tkinter import ttk
import random
import colorsys
import matplotlib
import pickle


# define the player class, with name, score and x and y coordinates, add debug function printPlayer()

class player:
    def __init__(self, name, scr, color):
        self.name = name
        self.scr = scr
        self.x = 0
        self.y = 0
        self.color = color
        self.fg='#FFFFFF'
        self.factor = 1.9
        self.kiset = False
    def printPlayer(self):
        return ''+self.name+': '+str(self.scr)+', aktuelle Position: '+str(self.x+1)+'|'+str(self.y+1)


# this function sets the colors for the players, first at init and also every move or return

def colorscale(hexa, amount):
    rgb=matplotlib.colors.ColorConverter.to_rgb(hexa)
    h,l,s = colorsys.rgb_to_hls(*rgb)
    l = min(1, l * amount)
    rgb=colorsys.hls_to_rgb(h,l,s)
    r = rgb[0]*255
    g = rgb[1]*255
    b = rgb[2]*255

    r = format(int(r), '02x')
    g = format(int(g), '02x')
    b = format(int(b), '02x')
    return '#'+r+g+b

    
# if a column (or row) is empty, this checks who won

def checkWincon():
    global currPly, root, winLabel,win
    summe = 0
    if not currPly:
        for i in range(8):
            summe+=values[players[1].x][i]      # sums all values in a row
    else:
        for i in range(8):
            summe+=values[i][players[0].y]      # sums all values in a column
    if summe==-160:                             # if sum is -160 (=> all fields empty) finish game
        p1scr = players[0].scr                  # get player scores
        p2scr = players[1].scr                  
        if p1scr>p2scr:                         # finds out who won or if it is a draw
            winstr = players[0].name + ' won!!!'
            foreg = players[0].color
        elif p1scr==p2scr:
            winstr = 'It\'s a draw!!!'
            foreg = '#000000'
        else:
            winstr = players[1].name + ' won!!!'
            foreg = players[1].color 
        winLabel.config(text=winstr, fg=foreg)
        win = True

# short function to make the score string easier

def getScoreString(p):
    return p.name + ": "+str(p.scr)

# this handles the key events

    # the first one the enter key event (take number) and sets the current player to the other value
    # 

def enterKeyPressed(event):
    global currPly, p1Label, players
    kiset = players[1].kiset
    if not kiset:         
        if not((values[players[0].x][players[0].y]==-20 and currPly) or (values[players[1].x][players[1].y]==-20 and not currPly)):
            if currPly:
                players[1].x = players[0].x
                players[1].y = players[0].y
                players[0].scr+=values[players[0].x][players[0].y]
                values[players[0].x][players[0].y] = -20
                fields[players[0].x][players[0].y].config(text = '')
            else:
                players[0].x = players[1].x
                players[0].y = players[1].y
                players[1].scr+=values[players[1].x][players[1].y]
                values[players[1].x][players[1].y] = -20
                fields[players[1].x][players[1].y].config(text = '')
            currPly = not currPly
            p1Label.config(text=getScoreString(players[0]))
            p2Label.config(text=getScoreString(players[1]))
            setColors()
            checkWincon()
    else:
        if values[players[0].x][players[0].y]!=-20:
            players[1].x = players[0].x
            players[1].y = players[0].y
            players[0].scr+=values[players[0].x][players[0].y]
            values[players[0].x][players[0].y] = -20
            fields[players[0].x][players[0].y].config(text = '')
            p1Label.config(text=getScoreString(players[0]))
            p2Label.config(text=getScoreString(players[1]))
            setColors()
            players[1].x = players[0].x
            players[1].y = players[0].y
            currPly = not currPly
            checkWincon()
            tempValues = []
            tempValues2 = [[]]
            takenFields = []
            for i in range(8):
                tempValues.append(values[players[0].x][i])
            for i in range(8):
                k = tempValues[i]
                m = i
                z = True
                for r in range(5):
                    tempValues2 = list(zip(*values[::-1])) if z else values
                    imax1 = tempValues2[m].index(max(tempValues2[m]))
                    k -= tempValues2[m][imax1] if z else -1*tempValues2[m][imax1]
                    m = tempValues2[m].index(max(tempValues2[m]))
                    z = not z
                takenFields.append(k)
            indexm = takenFields.index(max(takenFields))
            updown = True if indexm > players[0].y else False
            for i in range(abs(indexm-players[0].y-1)):
                if updown:
                    sKeyPressed(i)
                else:
                    wKeyPressed(i)
            players[1].scr+=tempValues[indexm]
            values[players[0].x][indexm]=-20
            fields[players[0].x][indexm].config(text='')
            players[0].x = players[1].x
            players[0].y = players[1].y
            players[1].y = indexm
            players[0].y = indexm
            currPly=not currPly
            setColors()
           
                    
            




    # the function wKeyPressed and sKeyPressed only works if player 2 is playing

def wKeyPressed(event):
    global currPly
    atleastonce = True
    if not currPly and not win:
        while(values[players[1].x][players[1].y]==-20 or atleastonce):
            atleastonce = False
            players[1].y-=1
            if players[1].y==-1:
                players[1].y=7
        setColors()
def sKeyPressed(event):
    global currPly
    atleastonce = True
    if not currPly and not win:
        while(values[players[1].x][players[1].y]==-20 or atleastonce):
            atleastonce = False
            players[1].y+=1
            if players[1].y==8:
                players[1].y=0
        setColors()
    # the function aKeyPressed and dKeyPressed only works if player 1 is playing

def aKeyPressed(event):
    global currPly
    atleastonce = True
    if currPly and not win:
        while(values[players[0].x][players[0].y]==-20 or atleastonce):
            atleastonce = False
            players[0].x-=1
            if players[0].x==-1:
                players[0].x=7
        setColors()
def dKeyPressed(event):
    global currPly
    atleastonce = True
    if currPly and not win:
        while(values[players[0].x][players[0].y]==-20 or atleastonce):
            atleastonce = False
            players[0].x+=1
            if players[0].x==8:
                players[0].x=0
        setColors()

def name1c(a,b,c):
    if name1T.get()!='':
        players[0].name=name1T.get()
    else:
        players[0].name='Spieler 1'
    p1Label.config(text=players[0].name + ': ' + str(players[0].scr))

def name2c(a,b,c):
    if name2T.get()!='':
        players[1].name=name2T.get()
    else:
        players[1].name='Spieler 2'
    
    p2Label.config(text=players[1].name + ': ' + str(players[1].scr))

def calcColor():
    global colBlue1,colBlue2,colBlue3,colRed1,colRed2,colRed3
    colBlue1 = colorscale(players[0].color,0.5) # color of current field: darkblue
    colBlue2 = colorscale(players[0].color,1.1) # color of fields in current row: a lighter blue
    colBlue3 = colorscale(players[0].color,1.5) # color of all borders around both of the above: very light blue

    # colors of (red) player 2

    colRed1 = colorscale(players[1].color,0.5)  # color of current field: darkred
    colRed2 = colorscale(players[1].color,1.1)  # color of fields in current column: a lighter red
    colRed3 = colorscale(players[1].color,1.5) # color of all borders around both of the above: very light red

def setColors():
    global fieldBorders, fields,colBlue1,colBlue2,colBlue3, currPly,colRed1,colRed2,colRed3
    for i in range(8):
        for j in range(8):
            fieldBorders[i][j].config(bg='#404040')
            fields[i][j].config(bg='#999999', fg='#FFFFFF')
    if currPly:
        fieldBorders[players[0].x][players[0].y].config(bg=colBlue3)
        fields[players[0].x][players[0].y].config(bg=colBlue1, fg=players[0].fg)
    else:
        fieldBorders[players[1].x][players[1].y].config(bg=colRed3)
        fields[players[1].x][players[1].y].config(bg=colRed1, fg=players[1].fg)

    for i in range(8):
        cp = 0 if currPly else 1
        if i != players[cp].x:
            fieldBorders[i][players[cp].y].config(bg=colBlue3)
            fields[i][players[cp].y].config(bg=colBlue2,fg=players[0].fg)
    for i in range(8):
        if i != players[cp].y:
            fieldBorders[players[cp].x][i].config(bg=colRed3)
            fields[players[cp].x][i].config(bg=colRed2,fg=players[1].fg)
    frame1.config(bg=colorscale(players[0].color,players[0].factor) if currPly else colorscale(players[1].color,players[1].factor))                                  # ?: <3 <3 <3
    p1Label.config(bg=colorscale(players[0].color,players[0].factor) if currPly else colorscale(players[1].color,players[1].factor))
    p1Label.config(fg=players[0].color)
    p2Label.config(bg=colorscale(players[0].color,players[0].factor) if currPly else colorscale(players[1].color,players[1].factor))
    p2Label.config(fg=players[1].color)
    winLabel.config(bg=colorscale(players[0].color,players[0].factor) if currPly else colorscale(players[1].color,players[1].factor))
    currPlyCanvas.config(bg=colorscale(players[0].color,players[0].factor) if currPly else colorscale(players[1].color,players[1].factor),highlightthickness=0)
    currPlyCanvas.itemconfig(p1Dot, fill=players[0].color if currPly else colorscale(players[1].color,players[1].factor))
    currPlyCanvas.itemconfig(p2Dot, fill=colorscale(players[0].color,players[0].factor) if currPly else players[1].color)
    wLabel.config(bg=players[1].color,fg=players[1].fg)
    sLabel.config(bg=players[1].color,fg=players[1].fg)
    aLabel.config(bg=players[0].color,fg=players[0].fg)
    dLabel.config(bg=players[0].color,fg=players[0].fg)
    name1L.config(fg=players[0].color)
    name2L.config(fg=players[1].color)


def colorP1rC(event):
    if players[1].color == '#FF0000':
        players[1].color = players[0].color
        players[1].fg = players[0].fg
        players[1].factor = players[0].factor
    players[0].color = '#FF0000'
    players[0].fg = '#FFFFFF'
    players[0].factor=1.9
    calcColor()
    setColors()

def colorP1gC(event):
    if players[1].color == '#00BA00':
        players[1].color = players[0].color
        players[1].fg = players[0].fg
        players[1].factor = players[0].factor
    players[0].color = '#00BA00'
    players[0].fg = '#000000'
    players[0].factor = 2.5
    calcColor()
    setColors()

def colorP1bC(event):
    if players[1].color == '#0000FF':
        players[1].color = players[0].color
        players[1].fg = players[0].fg
        players[1].factor = players[0].factor
    players[0].color = '#0000FF'
    players[0].fg = '#FFFFFF'
    players[0].factor=1.9
    calcColor()
    setColors()

def colorP1grC(event):
    if players[1].color == '#444444':
        players[1].color = players[0].color
        players[1].fg = players[0].fg
        players[1].factor = players[0].factor
    players[0].color = '#444444'
    players[0].fg = '#FFFFFF'
    players[0].factor = 2.5
    calcColor()
    setColors()

def colorP1vC(event):
    if players[1].color == '#B000B0':
        players[1].color = players[0].color
        players[1].fg = players[0].fg
        players[1].factor = players[0].factor
    players[0].color = '#B000B0'
    players[0].fg = '#FFFFFF'
    players[0].factor = 2.8
    calcColor()
    setColors()

def colorP1yC(event):
    if players[1].color == '#E3E300':
        players[1].color = players[0].color
        players[1].fg = players[0].fg
        players[1].factor = players[0].factor
    players[0].color = '#E3E300'
    players[0].fg = '#000000'
    players[0].factor=2.1
    calcColor()
    setColors()

def colorP2rC(event):
    if players[0].color == '#FF0000':
        players[0].color = players[1].color
        players[0].fg = players[1].fg
        players[0].factor = players[1].factor
    players[1].color = '#FF0000'
    players[1].fg = '#FFFFFF'
    players[1].factor=1.9
    calcColor()
    setColors()

def colorP2gC(event):
    if players[0].color == '#00BA00':
        players[0].color = players[1].color
        players[0].fg = players[1].fg
        players[0].factor = players[1].factor
    players[1].color = '#00BA00'
    players[1].fg = '#000000'
    players[1].factor = 2.5
    calcColor()
    setColors()

def colorP2bC(event):
    if players[0].color == '#0000FF':
        players[0].color = players[1].color
        players[0].fg = players[1].fg
        players[0].factor = players[1].factor
    players[1].color = '#0000FF'
    players[1].fg = '#FFFFFF'
    players[1].factor=1.9
    calcColor()
    setColors()

def colorP2grC(event):
    if players[0].color == '#444444':
        players[0].color = players[1].color
        players[0].fg = players[1].fg
        players[0].factor = players[1].factor
    players[1].color = '#444444'
    players[1].fg = '#FFFFFF'
    players[1].factor = 2.5
    calcColor()
    setColors()

def colorP2vC(event):
    if players[0].color == '#B000B0':
        players[0].color = players[1].color
        players[0].fg = players[1].fg
        players[0].factor = players[1].factor
    players[1].color = '#B000B0'
    players[1].fg = '#FFFFFF'
    players[1].factor = 2.8
    calcColor()
    setColors()

def colorP2yC(event):
    if players[0].color == '#E3E300':
        players[0].color = players[1].color
        players[0].fg = players[1].fg
        players[0].factor = players[1].factor
    players[1].color = '#E3E300'
    players[1].fg = '#000000'
    players[1].factor=2.1
    calcColor()
    setColors()

# initialisation of player objects

try:
    infile = open('save','rb')
    players = pickle.load(infile)
    infile.close()
except:
    players = [player('Spieler 1',0,'#0000FF'), player('Spieler 2', 0, '#FF0000')]
    

# colors of (blue) player 1


# tkinter init


calcColor()
root = Tk()
root.title('MaxIt')  # title of the window
root.geometry('260x480') # dimension of the window
notebook = ttk.Notebook(root)
notebook.pack()
frame1 = Frame(notebook, width=260, height=450, pady=25)
frame2 = Frame(notebook, width=260, height=450, pady=25)
frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
notebook.add(frame1,text='Spiel')
notebook.add(frame2,text='Optionen')

# set win bool to false, becomes true if someone won to prevent continous loop

win = False

# bind the keyPress events

root.bind('<Return>', enterKeyPressed)
root.bind('w', wKeyPressed)
root.bind('s', sKeyPressed)
root.bind('a', aKeyPressed)
root.bind('d', dKeyPressed)

fields = [[]]
fieldBorders=[[]]
values = [[]]
currPly = True


# initialization of standart values of MaxIt
def startGame():
    global fields, fieldBorders, values, currPly
    fields = [[]]
    fieldBorders=[[]]
    values = [[]]
    stdNumbers=[-9,-7,-6,-6,-5,-5,-4,-4,-4,-3,-3,-3,-2,-2,-2,-2,-1,-1,-1,-1,-1,0,0,0,0,0,0,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7,7,7,8,8,9,9,10,15]

    # shuffle the values for a random field of numbers

    random.shuffle(stdNumbers)

    # initialization of arrays for the 8x8 Field of Labels, Borders and values

    
    # at the start of the game there is one free field, which is random, where the game begins

    freefield=[random.randint(0,7),random.randint(0,7)]
    players[0].x,players[0].y=freefield[0],freefield[1]
    currPly = True

    # the list of standard numbers contains only 63 Elements, so if the 64th is created (the free field) you have to subtract 1

    freefieldused = 0

    # create the 8x8 arrays containing the Labels, borders and values

    # iteration over all rows

    for j in range(8):

        # initialize temporary lists for all three
        
        tempList = []
        tempBorders = []
        tempValues = []

        # iterate over all columns in current row

        for i in range(8):

            # if (i,j) is the free field then set the label text to '', set freefieldused to 1 and change the value of that field to -20 (for bool comparison)

            if i==freefield[1] and j==freefield[0]:
                labeltext = ''
                freefieldused=1
                tempValues.append(-20)
            
            # if the condition above is not met, set the field text and value to the corresponding value in the standard value list

            else:
                labeltext = str(stdNumbers[j*8+i-freefieldused])
                tempValues.append(stdNumbers[j*8+i-freefieldused])

            # append a label (which serves as a border) to the temporary border list and set its color to a lighter grey

            tempBorders.append(Label(frame1,text='', bg='#404040'))

            # append a label with the corresponding value printed on it in a darker gray to the temporary field list. Set its font to "Bahnschrift" with size 16 and a white font color

            tempList.append(Label(frame1,text=labeltext, bg='#999999',fg='#FFFFFF',font=('Bahnschrift',16)))
            
            # place the created labels into the window
            
            tempBorders[i].place(x=10+30*j,y=100+30*i,width=29,height=29)
            tempList[i].place(x=10+30*j+2,y=100+30*i+2,width=25,height=25)

        # after iterating over the columns in current row, and thus creating complete 8 elements lists, append those to the permanent lists
        
        fields.append(tempList)
        fieldBorders.append(tempBorders)
        values.append(tempValues)

    # this is a probably avoidable bugfix, bc the first element of those lists was always empty

    fields.pop(0)
    fieldBorders.pop(0)
    values.pop(0)

def newGame():
    global win, currPly
    players[0].scr=0
    players[1].scr=0
    win=False
    currPly=True
    p1Label.config(text=players[0].name + ': ' + str(players[0].scr))
    p2Label.config(text=players[1].name + ': ' + str(players[1].scr))
    winLabel.config(text='')
    startGame()
    calcColor()
    setColors()

def closeGame():
    outfile = open('save','wb')
    players[0].scr=0
    players[1].scr=0
    pickle.dump(players,outfile)
    outfile.close()
    root.destroy()

def kiBc(a,b,c):
    global kiB, n2t
    kiBa=kiB.get()
    if kiBa==0:
        players[1].kiset = False
        players[1].name = 'Spieler 2'
        newGame()
    else:
        players[1].kiset = True
        players[1].name = 'Computer'
        newGame()
    n2t.set(players[1].name)


# make Labels for other UI Element: Score, Current Player Dot, Instructions, Button to close
startGame()
p1Label = Label(frame1,text=players[0].name + ': ' + str(players[0].scr), fg=players[0].color, font='Bahnschrift 13 bold')
p2Label = Label(frame1,text=players[1].name + ': ' + str(players[1].scr), fg=players[1].color, font='Bahnschrift 13 bold')
p1Label.place(x=40,y=10)
p2Label.place(x=40,y=40)
currPlyCanvas = Canvas(frame1)
currPlyCanvas.place(x=20,y=10,width=20,height=55)
p1Dot = currPlyCanvas.create_oval(5,8,15,18,outline='', fill='#0000FF')
p2Dot = currPlyCanvas.create_oval(5,39,15,49,outline='', fill='#BBBFDE')
wLabel = Label(frame1,text="w",font='Bahnschrift 13 bold', bg=colRed2, fg=players[1].fg)
wLabel.place(x=170,y=17,width=20, height=20)
sLabel = Label(frame1,text="s",font='Bahnschrift 13 bold', bg=colRed2, fg=players[1].fg)
sLabel.place(x=170,y=42,width=20, height=20)
aLabel = Label(frame1,text="a",font='Bahnschrift 13 bold', bg=colBlue2, fg=players[0].fg)
aLabel.place(x=145,y=42,width=20, height=20)
dLabel = Label(frame1,text="d",font='Bahnschrift 13 bold', bg=colBlue2, fg=players[0].fg)
dLabel.place(x=195,y=42,width=20, height=20)
retLabel = Label(frame1, text='⏎', font='Bahnschrift 13 bold', bg='#606060', fg='#FFFFFF')
retLabel.place(x=225,y=17,width=20,height=45)

winLabel = Label(frame1,font='Bahnschrift 13 bold')
winLabel.place(x=10, y=70)
Button(frame1,text='Spiel beenden', command=closeGame).place(x=80,y=390, width=100)
Button(frame1,text='Neues Spiel', command=newGame).place(x=80,y=350, width=100)

nameL = Label(frame2, text='Namen', font='Bahnschrift 13 bold')
name1L = Label(frame2, text='Spieler 1:',font='Bahnschrift 13 bold', fg=players[0].color)
name2L = Label(frame2, text='Spieler 2:',font='Bahnschrift 13 bold', fg=players[1].color)

nameL.place(x=10,y=5)
name1L.place(x=10,y=30)
name2L.place(x=10,y=55)

colorName1 = Label(frame2, text='Farbe von Spieler 1',font='Bahnschrift 13 bold')

colorP1g = Label(frame2, text='',bg='#00BA00')
colorP1b = Label(frame2, text='',bg='#0000FF')
colorP1r = Label(frame2, text='',bg='#FF0000')
colorP1gr = Label(frame2, text='',bg='#444444')
colorP1v = Label(frame2, text='',bg='#B000B0')
colorP1y = Label(frame2, text='',bg='#E3E300')

colorP1r.bind('<Button-1>', colorP1rC)
colorP1g.bind('<Button-1>', colorP1gC)
colorP1b.bind('<Button-1>', colorP1bC)
colorP1gr.bind('<Button-1>',colorP1grC)
colorP1v.bind('<Button-1>',colorP1vC)
colorP1y.bind('<Button-1>',colorP1yC)

colorName1.place(x=10,y=80)

colorP1r.place(x=15,y=105,width=25, height=25)
colorP1g.place(x=40,y=105,width=25, height=25)
colorP1b.place(x=65,y=105,width=25, height=25)
colorP1gr.place(x=90,y=105,width=25, height=25)
colorP1v.place(x=115,y=105,width=25, height=25)
colorP1y.place(x=140,y=105,width=25, height=25)

colorName2 = Label(frame2, text='Farbe von Spieler 2',font='Bahnschrift 13 bold')

colorP2g = Label(frame2, text='',bg='#00BA00')
colorP2b = Label(frame2, text='',bg='#0000FF')
colorP2r = Label(frame2, text='',bg='#FF0000')
colorP2gr = Label(frame2, text='',bg='#444444')
colorP2v = Label(frame2, text='',bg='#B000B0')
colorP2y = Label(frame2, text='',bg='#E3E300')

colorP2r.bind('<Button-1>', colorP2rC)
colorP2g.bind('<Button-1>', colorP2gC)
colorP2b.bind('<Button-1>', colorP2bC)
colorP2gr.bind('<Button-1>',colorP2grC)
colorP2v.bind('<Button-1>',colorP2vC)
colorP2y.bind('<Button-1>',colorP2yC)

colorName2.place(x=10,y=150)

colorP2r.place(x=15,y=175,width=25, height=25)
colorP2g.place(x=40,y=175,width=25, height=25)
colorP2b.place(x=65,y=175,width=25, height=25)
colorP2gr.place(x=90,y=175,width=25, height=25)
colorP2v.place(x=115,y=175,width=25, height=25)
colorP2y.place(x=140,y=175,width=25, height=25)


n1t = StringVar(value=players[0].name)
n1t.trace_add('write', name1c)

n2t = StringVar(value=players[1].name)
n2t.trace_add('write', name2c)

name1T = Entry(frame2, textvariable=n1t)
name2T = Entry(frame2, textvariable=n2t)
name1T.place(x=90,y=35)
name2T.place(x=90,y=60)

kiLabel = Label(frame2, text='Achtung: Auswählen startet\nneues Spiel!',font='Bahnschrift 13 bold')
kiB = IntVar(value=1 if players[1].kiset else 0)
kiCheckB = Checkbutton(frame2, text='Spieler 2 = KI?', variable=kiB,font='Bahnschrift 13 bold')
kiB.trace_add('write', kiBc)

kiCheckB.place(x=10,y=220)
kiLabel.place(x=10,y=245)

# set the colors and borders of the current row to the above defined first player colors.

calcColor()
setColors()


# start the tkinter mainloop and thus start the game

root.mainloop()