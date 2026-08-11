import tkinter as tk
import db
import main_page

def loginPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/brian.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Iniciar Sesión")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frMail = app.labelFrames(app.mainFr, "Nombre de Usuario:")
    frMail.configure(bg = "#000")
    frMail.pack(ipady = 5, ipadx = 5, padx = 100, pady = 10, fill = "x")

    userInput = app.inputs(frMail)
    userInput.pack(ipadx = 10, ipady = 5, padx = 5, fill = "x")

    frPass = app.labelFrames(app.mainFr, "Contraseña:")
    frPass.configure(bg = "#000")
    frPass.pack(ipady = 5, ipadx = 5, padx = 100, pady = 10, fill = "x")

    passInput = app.inputs(frPass)
    passInput.configure(show = "*")
    passInput.bind("<F12>", lambda e: db.login(userInput.get(), passInput.get(), app))
    passInput.pack(ipadx = 10, ipady = 5, padx = 5, fill = "x")

    buttonFr = app.frames(app.mainFr)
    buttonFr.configure(fg_color = "#000")
    buttonFr.columnconfigure(0, weight = 1)
    buttonFr.columnconfigure(1, weight = 1)
    buttonFr.pack(pady = 20, padx = 80, fill = "x")

    singin = app.buttons(buttonFr, "Iniciar sesión - <F12>")
    singin.configure(command = lambda:db.login(userInput.get(), passInput.get(), app))
    singin.grid(row = 0, column = 0, padx = 20, sticky = "ew")

    back = app.buttons(buttonFr, "Atrás")
    back.configure(command = lambda:main_page.mainPage(app))
    back.grid(row = 0, column = 1, padx = 20, sticky = "ew")

    btns = [singin, back]
    fun = [print, main_page.mainPage]
    args = [("login pressed",), (app,)]

    app.navegate(0, btns, fun, True, args)