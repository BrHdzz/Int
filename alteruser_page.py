import tkinter as tk
import db
import dashboard_page

def alterUserPage(app, attribute):
    app.deletePage(app.mainFr)

    frTitle = app.frames(app.mainFr)
    frTitle.configure(fg_color = "#2b2b2b")
    frTitle.pack(pady = 20, ipadx = 5, ipady = 5)

    img = app.images(frTitle, "images/yoyo.jpg", 100, 100)
    img.grid(padx = 10, column = 0, row = 0)

    frTitle2 = app.frames(frTitle)
    frTitle2.configure(fg_color = "#2b2b2b")
    frTitle2.grid(padx = 10, column = 1, row = 0)
    
    label = app.labelTitle(frTitle2, "Modificar Información")
    label.configure(bg = "#2b2b2b")
    label.grid(padx = 10, column = 0, row = 0)

    img1 = app.images(frTitle2, "images/jijijija.png", 25, 103)
    img1.grid(padx = 10, column = 0, row = 1, sticky = tk.E)

    input = None

    if attribute == 1:
        frName = app.labelFrames(app.mainFr, "Nombre:")
        frName.configure(bg = "#000")
        frName.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)

        input = app.inputs(frName)
        input.pack(ipadx = 10, ipady = 5)
    elif attribute == 2:
        frUname = app.labelFrames(app.mainFr, "Nombre de usuario (máximo 15 caracteres):")
        frUname.configure(bg = "#000")
        frUname.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)

        input = app.inputs(frUname)
        input.pack(ipadx = 10, ipady = 5)
    elif attribute == 3:
        frMail = app.labelFrames(app.mainFr, "Correo Electrónico:")
        frMail.configure(bg = "#000")
        frMail.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)

        input = app.inputs(frMail)
        input.pack(ipadx = 10, ipady = 5)
    elif attribute == 4:
        frPass = app.labelFrames(app.mainFr, "Contraseña (8 a 20 caracteres):")
        frPass.configure(bg = "#000")
        frPass.pack(ipady = 2, ipadx = 5, padx = 100, pady = 30)

        input = app.inputs(frPass)
        input.configure(show = "*")
        input.pack(ipadx = 10, ipady = 5)

    singin = app.buttons(app.mainFr, "Guardar")
    singin.configure(command = lambda:db.alter_user_info(app, input.get(), attribute))
    singin.pack(pady = 5, padx = 100, fill = "x")

    back = app.buttons(app.mainFr, "Atrás")
    back.configure(command = lambda:dashboard_page.dasboardPage(app))
    back.pack(pady = 5, padx = 100, fill = "x")

    btns = [singin, back]
    functions = [db.alter_user_info, dashboard_page.dasboardPage]
    args = [(app, input.get(), attribute), (app,)]

    app.navegate(0, btns, functions, True, args)