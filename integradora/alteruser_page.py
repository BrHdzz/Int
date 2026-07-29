import tkinter as tk
import db
import dashboard_page

def alterUserPage(app, attribute):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.config(bg = "#000")
    frTitle.pack(pady = 20)

    img = app.images(frTitle, "images/yoyo.jpg", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.config(bg = "#000")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Modificar Información")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 0, row = 1, sticky = tk.E)

    input = None

    if attribute == 1:
        frName = app.labelFrames(app.mainFr, "Nombre:")
        frName.config(bg = "#000")
        frName.pack(ipady = 2, ipadx = 5, padx = 100, pady = 10)

        input = app.inputs(frName)
        input.pack(ipadx = 10, ipady = 5)
    elif attribute == 2:
        frUname = app.labelFrames(app.mainFr, "Nombre de usuario (máximo 15 caracteres):")
        frUname.config(bg = "#000")
        frUname.pack(ipady = 2, ipadx = 5, padx = 100, pady = 10)

        input = app.inputs(frUname)
        input.pack(ipadx = 10, ipady = 5)
    elif attribute == 3:
        frMail = app.labelFrames(app.mainFr, "Correo Electrónico:")
        frMail.config(bg = "#000")
        frMail.pack(ipady = 2, ipadx = 5, padx = 100, pady = 10)

        input = app.inputs(frMail)
        input.pack(ipadx = 10, ipady = 5)
    elif attribute == 4:
        frPass = app.labelFrames(app.mainFr, "Contraseña (8 a 20 caracteres):")
        frPass.config(bg = "#000")
        frPass.pack(ipady = 2, ipadx = 5, padx = 100, pady = 10)

        input = app.inputs(frPass)
        input.config(show = "*")
        input.pack(ipadx = 10, ipady = 5)

    buttonFr = app.frames(app.mainFr)
    buttonFr.config(bg = "#000")
    buttonFr.pack(expand = True, pady = 20)

    singin = app.buttons(buttonFr, "Guardar")
    singin.config(width = 20, command = lambda:db.alter_user_info(app, input.get(), attribute))
    singin.grid(row = 0, column = 0, padx = 20)

    back = app.buttons(buttonFr, "Atrás")
    back.config(width = 20, command = lambda:dashboard_page.dasboardPage(app))
    back.grid(row = 0, column = 1, padx = 20)