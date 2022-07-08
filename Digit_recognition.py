from tkinter import *
import Digit_recognition_backend
import numpy

inputSize = 28
pixelSize = 20
buttonH = 5
buttonW = 10
canvasWidth = canvasHeight = pixelSize*inputSize
black = "#000000"
white = "#ffffff"

colour_change_speed = 48 
brushSize = 2.5
sign = 1

cm = []
tl = []
results = [0,0,0,0,0,0,0,0,0,0]

for i in range(inputSize):
    cm.append([])
    tl.append([])
    for j in range(inputSize):
        cm[i].append(0)
        tl[i].append("")
    #r1-3list will be used to draw predictions; r1 for bars to make a plot, r2 class labels, r3 for percentages
    r1list = []
    r2list = []
    r3list = []
for i in range(len(results)):
    r1list.append("")
    r2list.append("")
    r3list.append("")

def brushMode():
    global sign
    sign = 1
    eraserbutton.configure(bg = black, fg = white)
    brushbutton.configure(bg = white, fg = black)

def eraserMode():
    global sign
    sign = -1
    brushbutton.configure(bg = black, fg = white)
    eraserbutton.configure(bg = white, fg = black)

def reset():
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            cm[i][j] = 0
    drawAll()
            
def random():
    global cm
    cm = Digit_recognition_backend.give_random()
    drawAll()
    update_predictions()

def back_and_forth():
    global cm
    lista1 = cm
    lista2 = []
    for j in range(28):
        lista2.append([])
        for k in range(28):
            lista2[j].append(float(lista1[k][j])/255)
    lista2 = numpy.array(lista2)

    result = []
    for i in range(len(lista2)):
        result.append([])
        for j in range(len(lista2[i])):
            result[i].append(float(lista2[j][i])*255)
    cm = result
    drawAll()

def update_predictions():
    global results
    results = Digit_recognition_backend.predict_digit(cm)
    drawResults()

def drawtile(x,y):
    can.delete(tl[x][y])
    blue = int((cm[x][y]))
    colour = "#0000"
    if blue <16: 
        colour  += ("0" +str(hex(blue)[-1:]))
    else:
        colour += str(hex(blue)[-2:])
    tl[x][y] = can.create_rectangle(x*pixelSize,y*pixelSize,(x+1)*pixelSize,(y+1)*pixelSize, fill = colour)

def check_and_change(x,y,dmod):
    if 0<=x and x<inputSize and 0<=y and y<inputSize:
        changed = cm[x][y]+colour_change_speed*sign*dmod
        if changed>=0 and changed<256:
            cm[x][y] = changed 
            drawtile(x,y)

def indraw(event):
    x = int(event.x/pixelSize)
    y = int(event.y/pixelSize)
    for i in range(inputSize):
        for j in range(inputSize):
            dist = abs(i-x)**2+abs(j-y)**2
            if dist<brushSize:
                check_and_change(i,j,(brushSize-dist)/brushSize)

def drawAll():
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            drawtile(i,j)

def drawResults():
    rowW = canvasWidth//4
    rowH = canvasHeight//((len(results)*2)+5)

    j = 0
    for i in range(len(results)*2+2):
        if i>2 and i%2 == 1:
            rescan.delete(r1list[j])
            rescan.delete(r2list[j])
            rescan.delete(r3list[j])
            r1list[j] = rescan.create_rectangle(rowW//2,i*rowH,rowW//2 + (rowW*results[j])//1,(i+1)*rowH,fill = "#2727ff")
            r2list[j] = rescan.create_text(rowW//2-10,((i+1/2)*rowH)//1, text = str(j), anchor = "e", fill = white)
            r3list[j] = rescan.create_text(rowW//2+10,((i+1/2)*rowH)//1, text = str(int(results[j]*100))+"%", anchor = "w", fill = white)
            j+=1


main_window = Tk()
main_window.title("Digit recognition")
main_window.configure(bg = black)

can = Canvas(main_window,width=canvasWidth,height=canvasHeight)
can.grid(row = 0, column = 0,rowspan = 5)

eraserbutton = Button(main_window, width = buttonW, height = buttonH, text = "Eraser",command = eraserMode, bg = black, fg = white, borderwidth = 10)
eraserbutton.grid(row = 0, column = 1, sticky = 'n')

brushbutton = Button(main_window, width = buttonW, height = buttonH, text = "Brush", command = brushMode, bg = white, fg = black, borderwidth = 10)
brushbutton.grid(row = 1, column = 1)

resetbutton = Button(main_window, width = buttonW, height = buttonH, text = "Reset", command = reset, bg = black, fg = white, borderwidth = 10)
resetbutton.grid(row = 2, column = 1)

randombutton = Button(main_window, width = buttonW, height = buttonH, text = "Random \n digit", command = random, bg = black, fg = white, borderwidth = 10)
randombutton.grid(row = 3, column = 1)

updatebutton = Button(main_window, width = buttonW, height = buttonH, text = "Update \n predictions", command = update_predictions, bg = black, fg = white, borderwidth = 10)
updatebutton.grid(row = 4, column = 1, sticky = 's')

rescan = Canvas(main_window,width=canvasWidth//2,height=canvasHeight,bg = black)
rescan.grid(row = 0, column = 2,rowspan = len(results)+1)


drawAll()
can.bind("<B1-Motion>",indraw)

main_window.mainloop()

