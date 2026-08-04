import tkinter as tk
from PIL import Image, ImageTk
import obj
import random
import pygame
from pygame import mixer
from games import result

class WhackMole:
    def __init__(self, app, xp, id):
        self.app = app
        self.xp = xp
        self.id = id
        self.h = obj.root.winfo_height()
        self.w = obj.root.winfo_width()
        self.time = 60
        self.overlapping = ()

        self.bgAudio = mixer
        self.pygame = pygame

        if not self.pygame.init():
            self.pygame.init()

        if not self.bgAudio.init():
            self.bgAudio.init()

        self.bgAudio.music.load("audio/whack_mole/bg.mp3")
        self.bgAudio.music.set_volume(0.1)
        self.bgAudio.music.play()

        fr = tk.Frame(app.mainFr, bg = "#2b2b2b")
        fr.columnconfigure(0, weight = 1)
        fr.columnconfigure(2, weight = 1)
        fr.pack(fill = "x")

        self.scoreLB = tk.Label(fr, text = "Puntaje: 0", bg = "#2b2b2b", fg = "#fff", font = ("Inter", 20))
        self.scoreLB.grid(padx = 10, pady = 2, column = 0, row = 0)

        self.missLB = tk.Label(fr, text = "Fallos: 0", bg = "#2b2b2b", fg = "#fff", font = ("Inter", 20))
        self.missLB.grid(padx = 10, pady = 2, column = 1, row = 0)

        self.timeLB = tk.Label(fr, text = "Tiempo: 01:00", bg = "#2b2b2b", fg = "#fff", font = ("Inter", 20))
        self.timeLB.grid(padx = 10, pady = 2, column = 2, row = 0)

        self.canva = tk.Canvas(app.mainFr, bg = "#000")
        self.canva.pack(fill = "both", expand = True)
        self.canva.focus_set()

        self.player = Player(self)

        self.mole = []

        self.timer()
        self.mole_appear()
        self.mole_disappear()

        self.canva.bind("<Button-1>", self.mole_click)
    
    def start(self):
        self.app.deletePage(self.app.mainFr)

        WhackMole(self.app, self.xp, self.id)

    def mole_appear(self):
        self.mole.append(Mole(self))

        self.canva.after(1000, self.mole_appear)

    def mole_disappear(self):
        for i in self.mole[:]:
            if not i.it in self.overlapping:
                self.canva.delete(i.it)
                self.mole.remove(i)

                self.player.misses += 1
                self.missLB.config(text = f"Fallos: {self.player.misses}")

        self.canva.after(3000, self.mole_disappear)

    def mole_click(self, evt):
        self.canva = evt.widget

        x = self.canva.canvasx(evt.x)
        y = self.canva.canvasy(evt.y)

        self.overlapping = self.canva.find_overlapping(x, y, x + 1, y + 1)

        for item in self.overlapping:
            for i in self.mole[:]:
                if item == i.it:
                   self.mole.remove(i)

            self.canva.delete(item)
            self.player.score += 10
            self.scoreLB.config(text = f"Puntaje: {self.player.score}")

    def timer(self):
        self.time -= 1

        self.timeLB.config(text = f"Tiempo: 00:{self.time:02}")

        if self.time > 0:
            self.canva.after(1000, self.timer)
        else:
            self.bgAudio.stop()
            result.results(self.app, self.player.misses, self.player.score, self.id, self.xp)

class Player:
    def __init__(self, app):
        self.app = app
        self.score = 0
        self.misses = -1

class Mole:
    def __init__(self, app):
        self.app = app
        self.x = random.randint(200, self.app.w - 200)
        self.y = random.randint(200, self.app.h - 200)

        moles = [
            "images/games/whack_mole/mencho.png",
            "images/games/whack_mole/claudia.png",
            "images/games/whack_mole/amlo.png",
            "images/games/whack_mole/pantera.png",
            "images/games/whack_mole/awa.png"
        ]

        img = Image.open(moles[random.randint(0, (len(moles) - 1))])
        img = img.resize((150, 150))

        self.img = ImageTk.PhotoImage(img)
        self.it = self.app.canva.create_image(self.x, self.y, image = self.img)
        self.app.canva.coords(self.it, self.x, self.y)