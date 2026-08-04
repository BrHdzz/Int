import tkinter as tk
from PIL import Image, ImageTk
import obj
import random
from pygame import mixer
from games import result

class CatchMoney:
    def __init__(self, app, xp, id):
        self.app = app
        self.xp = xp
        self.id = id
        self.h = obj.root.winfo_height()
        self.w = obj.root.winfo_width()
        self.time = 60

        self.bgAudio = mixer

        if not self.bgAudio.init():
            self.bgAudio.init()

        self.bgAudio.music.load("audio/catch_money/bg.mp3")
        self.bgAudio.music.set_volume(0.2)
        self.bgAudio.music.play()

        fr = tk.Frame(app.mainFr, bg = "#000")
        fr.columnconfigure(0, weight = 1)
        fr.columnconfigure(2, weight = 1)
        fr.pack(fill = "x")

        self.scoreLB = tk.Label(fr, text = "Puntaje: 0", bg = "#000", fg = "#fff", font = ("Inter", 20))
        self.scoreLB.grid(padx = 10, pady = 2, column = 0, row = 0)

        self.missLB = tk.Label(fr, text = "Fallos: 0", bg = "#000", fg = "#fff", font = ("Inter", 20))
        self.missLB.grid(padx = 10, pady = 2, column = 1, row = 0)

        self.timeLB = tk.Label(fr, text = "Tiempo: 01:00", bg = "#000", fg = "#fff", font = ("Inter", 20))
        self.timeLB.grid(padx = 10, pady = 2, column = 2, row = 0)

        self.canva = tk.Canvas(app.mainFr, bg = "#000")
        self.canva.pack(fill = "both", expand = True)
        self.canva.focus_set()

        self.player = Player(self)

        self.money = []

        self.money_drop()
        self.timer()

        self.canva.bind("<Right>", self.player.right)
        self.canva.bind("<Left>", self.player.left)
        self.canva.bind("<d>", self.player.right)
        self.canva.bind("<a>", self.player.left)
        self.canva.bind("<D>", self.player.right)
        self.canva.bind("<A>", self.player.left)
    
    def start(self):
        self.app.deletePage(self.app.mainFr)

        CatchMoney(self.app, self.xp, self.id)

    def money_drop(self):
        if random.randint(1, 250) == 1:
            self.money.append(Money(self))

        for i in self.money[:]:
            i.falls()

            if self.canva.coords(i.it)[1] > self.h:
                self.player.misses += 1

                self.missLB.config(text = f"Fallos: {self.player.misses}")

                self.money.remove(i)
                self.canva.delete(i.it)
            elif self.canva.bbox(i.it)[1] in range(self.canva.bbox(self.player.it)[1], self.canva.bbox(self.player.it)[3]) or self.canva.bbox(i.it)[3] in range(self.canva.bbox(self.player.it)[1], self.canva.bbox(self.player.it)[3]):
                if self.canva.bbox(i.it)[0] in range(self.canva.bbox(self.player.it)[0], self.canva.bbox(self.player.it)[2]) or self.canva.bbox(i.it)[2] in range(self.canva.bbox(self.player.it)[0], self.canva.bbox(self.player.it)[2]):
                    self.player.score += 10

                    self.money.remove(i)
                    self.canva.delete(i.it)

                    self.scoreLB.config(text = f"Puntaje: {self.player.score}")

        self.canva.after(5, self.money_drop)

    def timer(self):
        self.time -= 1

        self.timeLB.config(text = f"Tiempo: 00:{self.time:02}")

        if self.time > 0:
            self.canva.after(1000, self.timer)
        else:
            result.results(self.app, self.player.misses, self.player.score, self.id, self.xp)

class Player:
    def __init__(self, app):
        self.app = app
        self.score = 0
        self.misses = 0
        self.x = self.app.w / 2
        self.y = self.app.h - 160

        img = Image.open("images/games/catch_money/player.png")
        img = img.resize((150, 150))
        self.img = ImageTk.PhotoImage(img)
        self.it = self.app.canva.create_image(self.x, self.y, image = self.img)

    def left(self, event):
        if self.x > 50:
            self.x -= 10
            self.app.canva.coords(self.it, self.x, self.y)

    def right(self, event):
        if self.x < self.app.w - 50:
            self.x += 10
            self.app.canva.coords(self.it, self.x, self.y)

class Money:
    def __init__(self, app):
        self.app = app
        self.x = random.randint(500, self.app.w - 500)
        self.y = 0

        img = Image.open("images/games/catch_money/money.png")
        img = img.resize((100, 36))
        self.img = ImageTk.PhotoImage(img)
        self.it = self.app.canva.create_image(self.x, self.y, image = self.img)

    def falls(self):
        self.y += 1
        self.app.canva.coords(self.it, self.x, self.y)