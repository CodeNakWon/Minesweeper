import tkinter as tk
from tkinter import messagebox
import numpy as np


class Mine:
    def __init__(self, y, x, canvas):
        Mine.cleanZones
        self.x = x
        self.y = y
        self.flag = 0
        self.isMine = False
        self.neighbor = 0
        self.canvas = canvas
        self.searched = False
        self.SQUARE = 30
        self.box = canvas.create_rectangle(self.x * self.SQUARE,
                                           self.y * self.SQUARE,
                                           (self.x + 1) * self.SQUARE,
                                           (self.y + 1) * self.SQUARE,
                                           fill="#aaaaff")
        self.text = self.canvas.create_text(self.x * self.SQUARE + self.SQUARE / 2,
                                            self.y * self.SQUARE + self.SQUARE / 2, text="", fill="Black",
                                            font="Times 12")

    def __del__(self):
        self.canvas.delete(self.box)
        self.canvas.delete(self.text)

    def setYX(self, y, x):
        self.x = x
        self.y = y

    def onLClick(self):
        return self.reveal()

    def winEffect(self):
        self.canvas.itemconfig(self.box, fill="Blue")
        self.canvas.itemconfig(self.text, text="", fill="Black", font="Times 12")

    def reveal(self):
        if self.isMine == True:
            self.canvas.itemconfig(self.box, fill="Red")
            return 0
        elif self.searched == False:
            self.searched = True
            self.canvas.itemconfig(self.box, fill="White")
            Mine.cleanZones -= 1
            if self.neighbor != 0:
                self.canvas.itemconfig(self.text, text=self.neighbor)
            return 1

    def onRClick(self):
        if self.flag == 0 and self.searched != True:
            self.canvas.itemconfig(self.text, text="!", fill="Green", font="Times 22 bold")
            self.flag = 1
            return 1

        elif self.flag == 1:
            self.canvas.itemconfig(self.text, text="", fill="Black", font="Times 12")
            self.flag = 0
            return -1

        else:
            return 0


class Game(tk.Frame):
    def __init__(self, master):

        super(Game, self).__init__(master)
        self.SQUARE = 30
        self.mineField = []
        self.row = 9
        self.col = 9
        self.find = 0
        self.isGameover = False
        self.isStarted = False
        self.startPoint = [1, 1]
        self.numMines = 10
        self.infoArea = 50
        self.width = self.col * self.SQUARE
        self.height = self.row * self.SQUARE
        self.canvas = tk.Canvas(self, bg='Gray',
                                width=self.width,
                                height=self.height + self.infoArea, )
        self.canvas.pack()
        self.pack()
        self.canvas.bind('<Button-1>', self.left_button)
        self.canvas.bind('<Button-3>', self.right_button)
        self.infoBox = self.canvas.create_rectangle(0, self.height, self.width, self.height + self.infoArea,
                                                    fill="Gray")
        self.infoText = self.canvas.create_text(self.width / 10, self.height + self.infoArea / 2,
                                                text="Find : 0 / " + str(self.numMines), anchor=tk.W, font="Times 23")
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="9*9", command=lambda: self.setlevel(1))
        filemenu.add_command(label="16*16", command=lambda: self.setlevel(2))
        filemenu.add_command(label="16*30", command=lambda: self.setlevel(3))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)
        self.begin()

    def setlevel(self, level):
        self.isStarted = False
        if level == 1:
            self.row = 9
            self.col = 9
            self.numMines = 10
        elif level == 2:
            self.row = 16
            self.col = 16
            self.numMines = 40
        elif level == 3:
            self.row = 16
            self.col = 30
            self.numMines = 99
        self.begin()

    def setMines(self):
        randmines = np.array(range(self.col * self.row))
        randmines = np.delete(randmines, self.startPoint[1]
                              * self.col + self.startPoint[0])  # 시작시 지뢰를 클릭하는 것을 방지
        mines = np.random.choice(randmines, self.numMines, replace=False)  # 비복원추출
        for m in mines:
            self.mineField[m // self.col][m % self.col].isMine = True
        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.mineField[i][j].isMine == True:
                    self.mineField[i][j].neighbor = -1
                    continue
                count = 0
                for yy in range(-1, 2):
                    for xx in range(-1, 2):
                        if i + yy < 0:
                            continue
                        if i + yy >= self.row:
                            continue
                        if j + xx < 0:
                            continue
                        if j + xx >= self.col:
                            continue
                        if self.mineField[i + yy][j + xx].isMine == True:
                            count += 1
                        self.mineField[i][j].neighbor = count

    def begin(self):
        Mine.cleanZones = self.col * self.row - self.numMines
        self.isGameover = False
        self.isStarted = False
        self.find = 0
        self.height = self.row * self.SQUARE
        self.width = self.col * self.SQUARE
        self.canvas.configure(width=self.width,
                              height=self.height + self.infoArea)
        self.mineField = np.arange(self.row * self.col, dtype=Mine).reshape(self.row, self.col)
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.mineField[i][j] = Mine(i, j, self.canvas)
        self.reDrawInfoBox()
        self.updateInfo()

    def detect_region(self, y, x):
        self.mineField[y][x].reveal()
        self.mineField[y][x].searched = True
        for yy in range(-1, 2):
            for xx in range(-1, 2):
                if x + xx < 0:
                    continue
                if x + xx >= self.col:
                    continue
                if y + yy < 0:
                    continue
                if y + yy >= self.row:
                    continue
                if self.mineField[y + yy][x + xx].flag != 0:
                    continue
                elif self.mineField[y + yy][x + xx].neighbor != -1 and self.mineField[y + yy][
                    x + xx].searched == False and self.mineField[y][x].neighbor == 0:
                    self.detect_region(y + yy, x + xx)
                elif self.mineField[y + yy][x + xx].neighbor == 0 and self.mineField[y + yy][x + xx].searched == False:
                    self.detect_region(y + yy, x + xx)

    def left_button(self, event):
        if self.isGameover:
            return
        x = event.x // self.SQUARE
        y = event.y // self.SQUARE
        if x > self.col - 1 or y > self.row - 1:
            return
        if not self.isStarted:
            self.startPoint = [x, y]
            self.setMines()
            self.isStarted = True
        if self.mineField[y][x].flag == 1 or self.mineField[y][x].searched == True:
            return
        game = self.mineField[y][x].onLClick()
        if (self.mineField[y][x].neighbor == 0):
            self.detect_region(y, x)
        if Mine.cleanZones == 0:
            self.gameOver(True)
        if game == 0:
            self.gameOver(False)
        self.updateInfo()

    def reDrawInfoBox(self):  # 레벨이 초기화 될때 현황판 위치 조절
        self.canvas.coords(self.infoBox, 0, self.height, self.width, self.height + self.infoArea)
        self.canvas.coords(self.infoText, self.width / 10, self.height + self.infoArea / 2)

    def updateInfo(self):  # 발견한 지뢰 수를 갱신
        text = "Find : " + str(self.find) + " / " + str(self.numMines)
        self.canvas.itemconfig(self.infoText, text=text)

    def right_button(self, event):
        if self.isGameover:
            return
        x = event.x // self.SQUARE
        y = event.y // self.SQUARE
        if x > self.col or y > self.row or self.isStarted == False:
            return
        self.find += self.mineField[y][x].onRClick()
        self.updateInfo()

    def gameOver(self, win):
        self.isGameover = True
        if win:
            for i in range(0, self.row):
                for j in range(0, self.col):
                    if (self.mineField[i][j].isMine == True):
                        self.after((i * self.col + j) * 5, self.mineField[i][j].winEffect)  # 승리시 게임종료 효과
            tk.messagebox.showinfo('Win', 'You Win!')
        else:
            for i in range(0, self.row):
                for j in range(0, self.col):
                    if (self.mineField[i][j].isMine == True):
                        self.after((i * self.col + j) * 5, self.mineField[i][j].reveal)  # 패배시 게임종료 효과 승리
            tk.messagebox.showinfo('Loose', 'You Loose!')
        self.begin()


root = tk.Tk()
root.title("mine")
game = Game(root)
game.mainloop()
