import tkinter as tk
import obj
import json
import os
import sigin_page
import login_page
import dashboard_page
import random
import db

splash_text = [
    "Los tiempos han cambiado... ohhh",
    "Abajo chatjepete, fuchi.",
    "Validate IP...",
    "Claudia Cheinbaun debería ser eterna.",
    "Ahh... Mi cacahuate.",
    "¡Los amo padres!",
    "Que rollo, plebes.",
    "Respeta a mi México más por favor.",
    "¡Viva la corrupción!",
    "Get a job.",
    "Ahí estan las masacres. :D",
    "Aplicación libre de IAzzzzzzzzzzzzzzzzz.",
    "No me pises, pa'."
]

def init(bar, app, l):
    bar["value"] = 0

    charge(bar, app, l)    

def charge(bar, app, l):
    if bar["value"] == 0:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 10:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 20:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 30:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 45:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 60:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 70:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
    elif bar["value"] == 80:
        i = random.randint(0, len(splash_text) - 1)

        l.configure(text = splash_text[i])

        splash_text.remove(splash_text[i])
            
    if bar["value"] < 100:
        bar["value"] += 1
        app.mainFr.after(50, charge, bar, app, l)
    else:
        if os.path.exists("session.json"):
            if os.path.getsize("session.json") >= 0:
                try:
                    with open("session.json") as f:
                        session = json.load(f)
                        
                        username = session["username"]
                        password = session["password"]
                    
                    db.login(username, password, app)
                except:
                    mainPage(app)

                    os.remove("session.json")
            else:
                os.remove("session.json")
        else:
            mainPage(app)

def keyboard(btn):
    btn.configure()
        
def splash(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#181818")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/logo.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#181818")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Modo Buenestar")
    label.configure(bg = "#181818")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    img2 = app.images(app.mainFr, "images/nega_logo.png", 200, 400)
    img2.pack(pady = 10)
    
    label = app.labelTxt(app.mainFr, "Cargando...")
    label.pack(pady = 20)
    
    label1 = app.labelTxt(app.mainFr, "")
    label1.pack(pady = 20)

    progBar = app.progressBars(app.mainFr)
    progBar.configure(length = 1000)
    progBar.pack(pady = 10)

    init(progBar, app, label1)

ind = 0

def mainPage(app):
    app.deletePage(app.mainFr)

    def delay():
        try:
            global ind

            title = [
                "Welcome", #inglés
                "Bienvenido", #español
                "Bienvenue", #francés
                "Benvenuto/Benvenuta", #italiano
                "Bem-vindo", #portugés
                "Willkommen", #alemán
                "ようこそ", #japones
                "어서 오세요", #chino
                "Добро пожаловать" #ruso
            ]

            txt = [
                "You may need someone to help you.",
                "Es posible que necesite ayuda de alguien.",
                "Vous aurez peut-être besoin de l'aide de quelqu'un.",
                "Potresti aver bisogno dell'aiuto di qualcuno.",
                "Você pode precisar da ajuda de alguém.",
                "Möglicherweise benötigen Sie Hilfe von jemandem.",
                "誰かの助けが必要になるかもしれません。",
                "你可能需要别人的帮助。",
                "Вам может понадобиться помощь."
            ]

            label.config(text = title[ind])
            label1.config(text = txt[ind])

            if ind == len(title) - 1: ind = 0
            else: ind += 1

            app.mainFr.after(3000, delay)
        except:
            pass

    label = app.labelTitle(app.mainFr, "")
    label.pack(pady = 5)

    img = app.images(app.mainFr, "images/main.png", 300, 300)
    img.pack(pady = 20, expand = True)

    label1 = app.labelTxt(app.mainFr, "")
    label1.config(font = ("Inter", 14, "italic"))
    label1.pack(pady = 5)

    buttonFr = app.frames(app.mainFr)
    buttonFr.configure(fg_color = "#000")
    buttonFr.columnconfigure(0, weight = 1)
    buttonFr.columnconfigure(1, weight = 1)
    buttonFr.pack(fill = "x", padx = 80, pady = 50)

    singin = app.buttons(buttonFr, "Registrarse")
    singin.configure(command = lambda:sigin_page.signinPage(app))
    singin.grid(row = 0, column = 0, padx = 20, sticky = "ew")

    login = app.buttons(buttonFr, "Iniciar sesión")
    login.configure(command = lambda:login_page.loginPage(app))
    login.grid(row = 0, column = 1, padx = 20, sticky = "ew")

    btns = [singin, login]
    functions = [sigin_page.signinPage, login_page.loginPage]
    args = [(app,), (app,)]

    app.navegate(0, btns, functions, True, args)

    delay()

global app

if __name__ == "__main__":
    app = obj.Window(obj.root, "Buenestar", "#000")
    
    splash(app)

    obj.root.mainloop()