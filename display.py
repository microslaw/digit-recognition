from tkinter import *
import numpy as np
import globals



class Display:

    def __init__(self, **kwargs):
        self.cm = np.zeros(globals.input_shape[:2])
        self.tl = [["" for _ in range(globals.inputSize)] for _ in range(globals.inputSize)]
        self.results = np.zeros(globals.num_classes)

        # r1-3list will be used to draw predictions; r1 for bars to make a plot, r2 class labels, r3 for percentages
        self.r1list = ["" for _ in range(globals.inputSize)]
        self.r2list = ["" for _ in range(globals.inputSize)]
        self.r3list = ["" for _ in range(globals.inputSize)]

        self.results = np.zeros(globals.num_classes)

        self.sign = 1

        self.eraserbutton = None
        self.brushbutton = None
        self.can = None
        self.main_window = None

        self.backend_references = kwargs

        self.init_canvas_elements()



    def brushMode(self):
        self.sign = 1
        self.eraserbutton.configure(bg=globals.black, fg=globals.white)
        self.brushbutton.configure(bg=globals.white, fg=globals.black)


    def eraserMode(self):
        self.sign = -1
        self.brushbutton.configure(bg=globals.black, fg=globals.white)
        self.eraserbutton.configure(bg=globals.white, fg=globals.black)


    def reset(self):
        self.cm = np.zeros(globals.input_shape[:2])
        self.drawAll()


    def random(self):
        self.cm = self.backend_references["random_digit"]()
        self.drawAll()
        self.update_predictions()

    def update_predictions(self):
        self.results = self.backend_references["predict"](self.cm)
        self.drawResults()


    def drawtile(self, x, y):
        self.can.delete(self.tl[x][y])
        blue = int((self.cm[x,y]))
        colour = "#0000"
        if blue < 16:
            colour += "0" + str(hex(blue)[-1:])
        else:
            colour += str(hex(blue)[-2:])
        self.tl[x][y] = self.can.create_rectangle(
            x * globals.pixelSize,
            y * globals.pixelSize,
            (x + 1) * globals.pixelSize,
            (y + 1) * globals.pixelSize,
            fill=colour,
        )


    def check_and_change_tile(self, x, y, dmod):
        if 0 <= x and x < globals.inputSize and 0 <= y and y < globals.inputSize:
            changed = self.cm[x][y] + globals.colour_change_speed * self.sign * dmod
            if changed >= 0 and changed < 256:
                self.cm[x][y] = changed
                self.drawtile(x, y)


    #reconsider
    def indraw(self, event):
        x = int(event.x / globals.pixelSize)
        y = int(event.y / globals.pixelSize)
        for i in range(globals.inputSize):
            for j in range(globals.inputSize):
                dist = abs(i - x) ** 2 + abs(j - y) ** 2
                if dist < globals.brushSize:
                    self.check_and_change_tile(i, j, (globals.brushSize - dist) / globals.brushSize)

    #reconsider
    def drawAll(self):
        for i in range(len(self.cm)):
            for j in range(len(self.cm[i])):
                self.drawtile(i, j)

    #reconsider
    def drawResults(self):
        rowW = globals.canvasWidth // 4
        rowH = globals.canvasHeight // ((len(self.results) * 2) + 5)

        j = 0
        for i in range(len(self.results) * 2 + 2):
            if i > 2 and i % 2 == 1:
                self.rescan.delete(self.r1list[j])
                self.rescan.delete(self.r2list[j])
                self.rescan.delete(self.r3list[j])
                self.r1list[j] = self.rescan.create_rectangle(
                    rowW // 2,
                    i * rowH,
                    rowW // 2 + (rowW * self.results[j]) // 1,
                    (i + 1) * rowH,
                    fill="#2727ff",
                )
                self.r2list[j] = self.rescan.create_text(
                    rowW // 2 - 10,
                    ((i + 1 / 2) * rowH) // 1,
                    text=str(j),
                    anchor="e",
                    fill=globals.white,
                )
                self.r3list[j] = self.rescan.create_text(
                    rowW // 2 + 10,
                    ((i + 1 / 2) * rowH) // 1,
                    text=str(int(self.results[j] * 100)) + "%",
                    anchor="w",
                    fill=globals.white,
                )
                j += 1

    #reconsider this one
    def button_factory(self, text, command):
        return Button(
            self.main_window,
            width=globals.buttonW,
            height=globals.buttonH,
            text=text,
            command=command,
            bg=globals.black,
            fg=globals.white,
            borderwidth=10,
        )

    #reconsider
    def init_canvas_elements(self):

        self.main_window = Tk()
        self.main_window.title("Digit recognition")
        self.main_window.configure(bg=globals.black)

        self.can = Canvas(self.main_window, width=globals.canvasWidth, height=globals.canvasHeight)
        self.can.grid(row=0, column=0, rowspan=5)

        self.eraserbutton = self.button_factory("Eraser", self.eraserMode)
        self.eraserbutton.grid(row=0, column=1, sticky="n")

        self.brushbutton = self.button_factory("Brush", self.brushMode)
        self.brushbutton.grid(row=1, column=1)

        self.resetbutton = self.button_factory("Reset", self.reset)
        self.resetbutton.grid(row=2, column=1)

        self.randombutton = self.button_factory("Random \n digit", self.random)
        self.randombutton.grid(row=3, column=1)

        self.updatebutton = self.button_factory("Update \n predictions", self.update_predictions)
        self.updatebutton.grid(row=4, column=1, sticky="s")

        self.rescan = Canvas(
            self.main_window,
            width=globals.canvasWidth // 2,
            height=globals.canvasHeight,
            bg=globals.black,
        )
        self.rescan.grid(row=0, column=2, rowspan=len(self.results) + 1)

        self.brushMode()

        self.drawAll()
        self.can.bind("<B1-Motion>", self.indraw)

