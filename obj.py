import tkinter as tk
import customtkinter as ctk
from tkextrafont import Font
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import var_config
import pyttsx3
import queue
import subprocess

def windowClose():
    Window.destroy()

class Window:
    def __init__(self, root, title, bg):
        self.root = root
        self.root.resizable(False, False)
        self.root.attributes("-fullscreen", True)
        self.root.geometry("100x100")
        self.root.iconphoto(True, tk.PhotoImage(file = "images/icon.png"))
        self.root.title(title)
        self.root.config(bg = bg)

        self.fr_close = tk.Frame(self.root, bg = "#1a1a1a")
        self.fr_close.pack(fill = "x")
        self.fr_close.columnconfigure(0, weight = 1)
        self.fr_close.columnconfigure(1, weight = 1)

        self.root.bind("<F4>", lambda e: self.root.destroy())
        
        tk.Label(self.fr_close, text = "App del Buenestar v1.0.16_02 - buenestarvb5piz3r.onion/", bg = "#1a1a1a", fg = "#008f1f", font = ("fonts/Syne.ttf", 12)).grid(row = 0, column = 0, sticky = "w")

        self.closeButtonWindow = ctk.CTkButton(self.fr_close, text = "X", corner_radius = 6, fg_color = "#2600cf", hover_color = "#14006b", text_color = "#fff", font = ("Inter", 20, "bold"), command = lambda:self.root.destroy())
        self.closeButtonWindow.grid(row = 0, column = 1, sticky = tk.E, ipady = 2)

        self.mainFr = tk.Frame(self.root, bg = "#000")
        self.mainFr.pack(expand = True, fill = "both")
        self.image = {}
        self.gif = {}
        self.loop = []

        self.index_nav = 0

    def play_tts(self, text):
        subprocess.Popen([
            "powershell",
            "-Command",
            f'Add-Type -AssemblyName System.Speech; '
            f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            f'$speak.Speak("{text}")'
        ])

    def navegate(self, x, array, fun, reset, args):
        if reset:
            arr = 0
            self.index_nav = 0
            self.root.unbind("<Return>")
            self.root.unbind("<space>")
        else:
            arr = len(array) - 1

            if arr == 0:
                array[self.index_nav].configure(fg_color = "#5d38ff")
            else:
                if 0 <= self.index_nav + x <= arr:
                    self.index_nav += x
                    array[self.index_nav].configure(fg_color = "#5d38ff")
                    array[self.index_nav - x].configure(fg_color = "#38b6ff")
                elif self.index_nav + x < 0:
                    self.index_nav = arr
                    array[self.index_nav].configure(fg_color = "#5d38ff")
                    array[0].configure(fg_color = "#38b6ff")
                elif self.index_nav + x > arr:
                    self.index_nav = 0
                    array[self.index_nav].configure(fg_color = "#5d38ff")
                    array[arr].configure(fg_color = "#38b6ff")

            print(self.index_nav)

            self.root.bind("<Return>", lambda e: fun[self.index_nav](*args[self.index_nav]))
            self.root.bind("<space>", lambda e: self.play_tts(array[self.index_nav].cget("text")))

        self.root.bind("<Up>", lambda e: self.navegate(-1, array, fun, False, args))
        self.root.bind("<Down>", lambda e: self.navegate(1, array, fun, False, args))

    def images(self, parent, image, h, w):
        key = (image, h, w)

        if key not in self.image:
            img = Image.open(image)
            img = img.resize((w, h))
            self.image[key] = ImageTk.PhotoImage(img)

        return tk.Label(parent, image = self.image[key], bg = "#000")

    def gifs(self, parent, gif, h, w):
        key = (gif, h, w)

        if key not in self.gif:
            img = Image.open(gif)

            fps = []

            lb = tk.Label(parent, bg = "#000")

            for frame in ImageSequence.Iterator(img):
                frameR = frame.copy().resize((w, h), Image.Resampling.LANCZOS)

                fps.append(ImageTk.PhotoImage(frameR))

            self.gif[key] = {
                "frame": fps,
                "index": 0,
                "duration": img.info.get("duration", 100),
                "label": lb
            }

            self.animGif(parent, key)
        else:
            lb = tk.Label(parent, bg = "#000")

            self.gif[key]["label"] = lb
            self.animGif(parent, key)

        return lb

    def animGif(self, parent, key):
        if key in self.gif:
            data = self.gif[key]
            index = data["index"]
            photo = data["frame"][index]

            data["label"].config(image = photo)
            data["index"] = (index + 1) % len(data["frame"])

            if parent.winfo_exists():
                self.loop.append(parent.after(data["duration"], self.animGif, parent, key))

    def frames(self, parent):
        return ctk.CTkFrame(parent)

    def framesTk(self, parent):
        return tk.Frame(parent)
    
    def labelTitle(self, parent, txt):
        return tk.Label(parent, text = txt, bg = "#000000", fg = "#5e17eb", font = (font.actual()["family"], var_config.fontSizeTitle))
    
    def labelTxt(self, parent, txt):
        return tk.Label(parent, text = txt, bg = "#000000", fg = "#ffffff", font = ("Inter", var_config.fontSizeText))
    
    def buttons(self, parent, txt):
        return ctk.CTkButton(parent, text = txt, corner_radius = 5, fg_color = "#38b6ff", hover_color = "#5d38ff", text_color = "#000", font = ("Inter", 30, "bold"), height = 60)

    def inputs(self, parent):
        return tk.Entry(parent, width = 50, border = 0, bg = "#2b2b2b", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), justify = "center", highlightbackground = "#2b2b2b", highlightcolor = "#de38ff", highlightthickness = 2, takefocus = True)
        
    def labelFrames(self, parent, txt):
        return tk.LabelFrame(parent, text = txt, border = 2, bg = "#000", fg = "#cb6ce6", highlightcolor = "#5e17eb", font = ("Inter", (var_config.fontSizeText - 1)))
    
    def scrollBars(self, parent):
        return tk.Scrollbar(parent, orient = tk.VERTICAL)
    
    def texts(self, parent, sc):
        return tk.Text(parent, bg = "#2b2b2b", fg = "#ffffff", font = ("Inter", var_config.fontSizeText), yscrollcommand = sc.set)
    
    def canvas(self, parent, sc):
        return tk.Canvas(parent, bg = "#000", yscrollcommand = sc.set, highlightthickness = 0)
    
    def progressBars(self, parent):
        style = ttk.Style()

        style.theme_use("clam")

        style.configure("Crypto.Horizontal.TProgressbar", troughcolor = "#181818", background = "#cb6ce6")

        return ttk.Progressbar(parent, orient = "horizontal", length = 300, mode = "determinate", maximum = 100, style = "Crypto.Horizontal.TProgressbar")

    def deletePage(self, parent):
        for i in parent.winfo_children():
            i.destroy()

root = ctk.CTk()

font = Font(file = "fonts/Syne-Bold.ttf", family = "syne")