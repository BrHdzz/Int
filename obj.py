import tkinter as tk
import customtkinter as ctk
from tkextrafont import Font
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import var_config
import xbox_controller
import os
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
        self.closeButtonWindow()
        self.mainFr = tk.Frame(self.root, bg = "#000")
        self.mainFr.pack(expand = True, fill = "both")
        self.image = {}
        self.gif = {}
        self.loop = []
        self.controller_xbox = xbox_controller.Controller(self)
        self.shKey()
        self.hideKey()

        self.root.bind("<Tab>", self.next)
        self.root.bind("<Shift-Tab>", self.prev)

    def next(self, evt):
        evt.widget.tk_focusNext().focus()
        return "break"
    
    def prev(self, evt):
        evt.widget.tk_focusPrev().focus()
        return "break"
    
    def closeButtonWindow(self):
        imgCloseButton = Image.open("images/close.png")
        imgCloseButton = imgCloseButton.resize((30, 30))

        self.imgCloseButton = ImageTk.PhotoImage(imgCloseButton)

        fr_close = tk.Frame(self.root, bg = "#1a1a1a")
        fr_close.pack(fill = "x")
        fr_close.columnconfigure(0, weight = 1)
        fr_close.columnconfigure(1, weight = 1)
        
        tk.Label(fr_close, text = "App del Buenestar v1.0.16_02 - buenestarvb5piz3r.onion/", bg = "#1a1a1a", fg = "#008f1f", font = ("fonts/Syne.ttf", 12)).grid(row = 0, column = 0, sticky = tk.W)

        exitBtn = tk.Button(fr_close, image = self.imgCloseButton, bg = "#1a1a1a", border = 0, cursor = "hand2", activebackground = "#000", command = lambda:self.root.destroy())
        exitBtn.bind("<FocusIn>", lambda e:exitBtn.config(bg = "#38b6ff"))
        exitBtn.bind("<FocusOut>", lambda e:exitBtn.config(bg = "#000"))
        exitBtn.bind("<Enter>", lambda e:exitBtn.config(bg = "#38b6ff"))
        exitBtn.bind("<Leave>", lambda e:exitBtn.config(bg = "#000"))
        exitBtn.grid(row = 0, column = 1, sticky = tk.E)

        #self.exitBtn = ctk.CTkButton(fr_close, fg_color = "#7700ff", corner_radius = 10, font = ("Arial", 30), text = "X")
        #self.exitBtn.grid(row = 0, column = 1, sticky = tk.E)
    
    def shKey(self):
        path = "C:/Program Files/Common Files/miscrosoft shared/ink/TabTip.exe"

        if os.path.exists(path):
            subprocess.Popen(path)
        #subprocess.Popen([os.path.join(os.path.dirname(os.path.abspath(__file__)), "TabTip.exe")])
    
    def hideKey(self):
        os.system("taskkill /IM TabTip.exe /F >nul 2>&1")

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

    def tabView(self, parent):
        return ctk.CTkTabview(parent)
    
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