import db
import main_page
import tkinter as tk

def signinPage(app):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/brian.png", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Crear Cuenta")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 0, row = 1, sticky = tk.E)

    frName = app.labelFrames(app.mainFr, "Nombre:")
    frName.configure(bg = "#000")
    frName.pack(ipady = 3, ipadx = 5, padx = 100, pady = 10, fill = "x")

    nameInput = app.inputs(frName)
    nameInput.pack(ipadx = 10, ipady = 5, fill = "x", padx = 5)

    frUname = app.labelFrames(app.mainFr, "Nombre de usuario (máximo 15 caracteres):")
    frUname.configure(bg = "#000")
    frUname.pack(ipady = 3, ipadx = 5, padx = 100, pady = 10, fill = "x")

    unameInput = app.inputs(frUname)
    unameInput.pack(ipadx = 10, ipady = 5, fill = "x", padx = 5)

    frMail = app.labelFrames(app.mainFr, "Correo Electrónico:")
    frMail.configure(bg = "#000")
    frMail.pack(ipady = 3, ipadx = 5, padx = 100, pady = 10, fill = "x")

    mailInput = app.inputs(frMail)
    mailInput.pack(ipadx = 10, ipady = 5, fill = "x", padx = 5)

    frPass = app.labelFrames(app.mainFr, "Contraseña (8 a 20 caracteres):")
    frPass.configure(bg = "#000")
    frPass.pack(ipady = 3, ipadx = 5, padx = 100, pady = 10, fill = "x")

    passInput = app.inputs(frPass)
    passInput.configure(show = "*")
    passInput.pack(ipadx = 10, ipady = 5, fill = "x", padx = 5)

    buttonFr = app.frames(app.mainFr)
    buttonFr.configure(fg_color = "#000")
    buttonFr.columnconfigure(0, weight = 1)
    buttonFr.columnconfigure(1, weight = 1)
    buttonFr.pack(fill = "x", padx = 80, pady = 20)

    singin = app.buttons(buttonFr, "Registrarse")
    singin.configure(command = lambda:db.signin(nameInput.get(), passInput.get(), unameInput.get(), mailInput.get(), app))
    singin.grid(row = 0, column = 0, padx = 20, sticky = "ew")

    back = app.buttons(buttonFr, "Atrás")
    back.configure(command = lambda:main_page.mainPage(app))
    back.grid(row = 0, column = 1, padx = 20, sticky = "ew")

    btns = [singin, back]
    fun = [db.signin, main_page.mainPage]
    args = [(nameInput.get(), passInput.get(), unameInput.get(), mailInput.get(), app), (app,)]

    app.navegate(0, btns, fun, True, args)