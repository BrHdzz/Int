import tkinter as tk
import db
import main_page

def loginPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/brian.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Crear Cuenta")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 1, row = 1)

    frMail = app.labelFrames(app.mainFr, "Nombre de Usuario:")
    frMail.config(bg = "#000")
    frMail.pack(ipady = 2, ipadx = 5, padx = 100, pady = 10)

    userInput = app.inputs(frMail)
    userInput.pack(ipadx = 10, ipady = 5)

    frPass = app.labelFrames(app.mainFr, "Contraseña:")
    frPass.config(bg = "#000")
    frPass.pack(ipady = 2, ipadx = 5, padx = 100, pady = 10)

    passInput = app.inputs(frPass)
    passInput.config(show = "*")
    passInput.pack(ipadx = 10, ipady = 5)

    buttonFr = app.frames(app.mainFr)
    buttonFr.config(bg = "#000")
    buttonFr.pack(pady = 20)

    singin = app.buttons(buttonFr, "Iniciar sesión")
    singin.config(width = 20, command = lambda:db.login(userInput.get(), passInput.get(), app))
    singin.grid(row = 0, column = 0, padx = 20)

    back = app.buttons(buttonFr, "Atrás")
    back.config(width = 20, command = lambda:main_page.mainPage(app))
    back.grid(row = 0, column = 1, padx = 20)
